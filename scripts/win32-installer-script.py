# script based on install-pythoncard.py

import sys, os
from distutils.command.install import install
from distutils.dist import Distribution

def get_scripts_dir():
    cmd = install(Distribution())
    cmd.finalize_options()
    return cmd.install_scripts
    
try:
    # Note: the function get_special_folder_path is only available when this
    # script is run by the installer
    prg = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
except OSError:
    try:
        prg = get_special_folder_path("CSIDL_PROGRAMS")
    except OSError, reason:
        # give up - cannot install shortcuts
        print "cannot install shortcuts: %s" % reason
        sys.exit()


dest_dir = os.path.join(prg, "Aksy")

pythonw = os.path.join(sys.prefix, "pythonw.exe")

def create_sc(script, lnk):
    target = os.path.join(get_scripts_dir(), script)
    path = os.path.join(dest_dir, lnk)

    create_shortcut(target, "Aksui", path)
    file_created(path)

if __name__ == '__main__':
    if "-install" == sys.argv[1]:

        try:
            os.mkdir(dest_dir)
            directory_created(dest_dir)
        except OSError:
            pass

        # create_shortcut(target, description, filename[, arguments[,         #             
        # workdir[, iconpath[, iconindex]]]])
        
        # file_created(path)
        #  - register 'path' so that the uninstaller removes it
        
        # directory_created(path)
        #  - register 'path' so that the uninstaller removes it
        
        # get_special_folder_location(csidl_string)
        create_sc("aksy-ui.exe", "Aksui.lnk")
        create_sc("aksy-ui-script.py", "Aksui with console.lnk")

        print "Aksy shortcuts have been successfully installed in your start menu."

    elif "-remove" == sys.argv[1]:
        pass


