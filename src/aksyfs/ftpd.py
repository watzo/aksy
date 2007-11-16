#!/usr/bin/env python
from pyftpdlib import ftpserver
from aksyfs import common
from aksy.config import create_option_parser
from aksy.device import Devices
from aksy import fileutils

import fnmatch
import os, time, errno

import logging
LOG = logging.getLogger("aksy.aksyfs.ftpd")

class AksyFtpFS(common.AksyFS, ftpserver.AbstractedFS):
    def __call__(self):
        return AksyFtpFS(self.sampler)

    def __init__(self, sampler):
        common.AksyFS.__init__(self, sampler)
        self.root = ''
        self.cwd = '/'
        self.rnfr = None

    def translate(self, path):
        """Translate a 'virtual' FTP path into equivalent filesystem path. Take
        an absolute or relative path as input and return a full absolute file
        path.
        
        """
        if LOG.isEnabledFor(logging.DEBUG): 
            LOG.debug('translate %s', path)

        if not os.path.isabs(path):
            path = os.path.join(self.cwd, path)
        # For AksyFS only virtual paths exist
        return os.path.normpath(path).replace('\\', '/')

    def open(self, filename, mode):
        """Open a file returning its handler."""
        if LOG.isEnabledFor(logging.DEBUG): 
            LOG.debug('open(%s, %s)', filename, mode)
        if self.isdir(filename):
            raise IOError(errno.EINVAL, filename)
        if mode.find('r') != -1:
            return self.open_for_read(filename, mode)
        elif mode.find('w') != -1:
            return self.open_for_write(filename, mode)
        else:
            common.raiseException(errno.EINVAL)

    def exists(self, abspath):
        """Return True if the path exists."""
        try:
            self.getattr(abspath)
            return True
        except OSError:
            return False
        
    def isfile(self, abspath):
        """Return True if path is a file."""
        return not fileutils.is_dirpath(abspath)

    def isdir(self, abspath):
        """Return True if path is a directory."""
        return fileutils.is_dirpath(abspath)

    def chdir(self, abspath):
        """Change the current directory."""
        if LOG.isEnabledFor(logging.DEBUG): 
            LOG.debug("chdir ", abspath)
        i = 1
        while i < len(abspath):
            i = abspath.find('/', i)
            if i == -1: i = len(abspath)
            self.getattr(abspath[:i])
            i += 1
            
        self.cwd = abspath

    def remove(self, abspath):
        """Remove the specified file."""
        self.unlink(abspath)
    
    def getsize(self, abspath):
        """Return the size of the specified file in bytes."""
        return common.get_file_size(abspath)

    def getmtime(self, abspath):
        """Return the last modified time as a number of seconds since the
        epoch."""
        return common.START_TIME
           
    def glob1(self, dirname, pattern):
        """Return a list of files matching a dirname pattern non-recursively.
        Unlike glob.glob1 raises an exception if os.listdir() fails.
        """
        names = self.listdir(dirname)
        if pattern[0] != '.':
            names = filter(lambda x: x[0] != '.', names)
        return fnmatch.filter(names, pattern)

    # --- utility methods
    
    # Note that these are resource-intensive blocking operations so you may want
    # to override and move them into another process/thread in some way.

    def get_nlst_dir(self, abspath):
        """Return a directory listing in a form suitable for NLST command."""
        listing = '\r\n'.join(self.listdir(abspath))
        if listing:
            return listing + '\r\n'
        return ''

    def get_list_dir(self, abspath):
        """Return a directory listing in a form suitable for LIST command."""
        # if path is a file we return information about it
        if os.path.isfile(abspath):
            basedir, filename = os.path.split(abspath)
            listing = [filename]
        else:
            basedir = abspath
            listing = self.listdir(abspath)
        return self.format_list(basedir, listing)

    def format_list(self, basedir, listing):
        """Return a directory listing emulating "/bin/ls -lgA" UNIX command
        output.

        <basedir> is the absolute dirname, <listing> is a list of files
        contained in that directory.

        For portability reasons permissions, hard links numbers, owners and
        groups listed are static and unreliable but it shouldn't represent a
        problem for most ftp clients around.
        If you want reliable values on unix systems override this method and
        use other attributes provided by os.stat().
        This is how output appears to client:

        -rwxrwxrwx   1 owner    group         7045120 Sep 02  3:47 music.mp3
        drwxrwxrwx   1 owner    group               0 Aug 31 18:50 e-books
        -rwxrwxrwx   1 owner    group             380 Sep 02  3:40 module.py
        """
        result = []
        for basename in listing:
            f = os.path.join(basedir, basename)
            stat = self.getattr(f)

            # stat.st_mtime could fail (-1) if file's last modification time is
            # too old, in that case we return local time as last modification time.
            try:
                mtime = time.strftime("%b %d %H:%M", time.localtime(stat.st_mtime))
            except ValueError:
                mtime = time.strftime("%b %d %H:%M")

            if fileutils.is_dirpath(f):
                result.append("drwxrwxrwx   1 owner    group %15s %s %s\r\n" %(
                    '0', # no size
                    mtime, 
                    basename))
            else:
                result.append("-rw-rw-rw-   1 owner    group %15s %s %s\r\n" %(
                    stat.st_size, 
                    mtime, 
                    basename))
        return ''.join(result)

def main():
    parser = create_option_parser(usage='%prog [options]')
    parser.add_option("--ftp_host", nargs=1, dest="ftp_host",
      help="Server host or IP address to bind on. Only change if running in an isolated network!", default='localhost')
    parser.add_option("--ftp_port", nargs=1, dest="ftp_port",
      help="Server port to bind on.", default=2121)

    options = parser.parse_args()[0]

    authorizer = ftpserver.DummyAuthorizer()
    authorizer.add_anonymous('/', perm=('r', 'w'))

    address = (options.ftp_host, options.ftp_port)
    if options.ftp_host != 'localhost':
        import warnings
        warnings.warn('Running aksyftpd on non-local address %s' % options.ftp_host, RuntimeWarning)
    
    sampler = Devices.get_instance(options.sampler_type, options.connector)

    try:    
        ftp_handler = ftpserver.FTPHandler
        ftp_handler.authorizer = authorizer
        ftp_handler.banner = "aksyftpd (pyftpd version %s) ready." % ftpserver.__ver__
        ftp_handler.abstracted_fs = AksyFtpFS(sampler)

        ftpd = ftpserver.FTPServer(address, ftp_handler)
        ftpd.max_cons = 256
        ftpd.max_cons_per_ip = ftpd.max_cons 
        ftpd.serve_forever()
    finally:
        sampler.close()

if __name__ == "__main__":
    main()
