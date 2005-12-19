#!/usr/bin/python
import sys, os, os.path, StringIO
import sysex_info

"""This hairy piece of code generates python modules from command
specifications (that once were extracted from the Akai sysex documentation
pdf)
Usage: generate_module.py command_spec_file skip_replyspec

command_spec_file: see data/z48 for examples.
skip_replyspec: do not use the information in the command_spec_file for
return types (but use typed parsing, see the z48 manual 'data types' for
more details.
device_name: the name for the device
"""
def _arglist_helper(arglist):
    """Creates correct string rep
    """
    if len(arglist) == 1:
         return '(' + arglist[0] + ',)'
    else:
         return '(' + ', '.join(arglist) + ')'

def method_name_helper(desc):
    """ Creates a method based on the description
    """
    desc = desc.split(' ')
    return '_'.join([word.lower() for word in desc[0:3]])

def classname_helper(section_name):
    """ Creates classname based on the section name
    """
    names = section_name.split('_')
    return ''.join([name.capitalize() for name in names])

# could use ljust etc...
indent_block = "    "
sysex_module_name = 'aksy.devices.akai.sysex'
sysex_types_module_name = 'aksy.devices.akai.sysex_types'

file_in_name = sys.argv[1]
device_name = os.path.dirname(file_in_name)
device_id = sysex_info.devices[device_name]['device_id']
skip_replyspec = sysex_info.devices[device_name]['skip_replyspec']
userref_type = sysex_info.devices[device_name].get('userref_type', None)

if len(sys.argv)== 3:
    skip_replyspec = False
file_in = open( file_in_name, 'r')
file_preamble = open( 'preamble', 'r')
preamble = "".join(file_preamble.readlines())
file_preamble.close()
command_spec = open( 'commandspec', 'r')
commandspec = ", ".join(command_spec.readlines()[0].rstrip().split("\t"))
command_spec.close()

line = file_in.readline()

# Section data
section_name, section_desc = line.rstrip().split('\t')
destfile = section_name + '.py'

file_out = open(destfile, 'w')
file_out.writelines( "\n\"\"\" Python equivalent of akai section %s\n\n%s\n\"\"\"\n\n" % (section_name,section_desc))
testfile_out_name = 'test' + "_" + section_name + ".py"
testfile_out = open(testfile_out_name, "w")
testfile_out.writelines("from unittest import TestCase, TestLoader\n\n")
testfile_out.writelines("from aksy.device import Devices\n\n")

file_out.writelines( "%s\n" % preamble)
file_out.writelines( "import %s,%s\n\n" % (sysex_module_name, sysex_types_module_name))
file_out.writelines( "class %s:\n" % classname_helper(section_name))
testClassName = "Test%s" % classname_helper(section_name)
testfile_out.writelines( "class %s(TestCase):\n" %testClassName)
file_out.writelines( "%sdef __init__(self, %s):\n" % (indent_block, device_name))
testfile_out.writelines( "%sdef setUp(self):\n" % indent_block)
testfile_out.writelines( "%sif not hasattr(self, %s):\n" % (indent_block*2,device_name))
testfile_out.writelines( "%ssetattr(self, %s, Devices.get_instance(%s, 'usb'))\n\n" % (indent_block*3,device_name, device_name))
file_out.writelines( "%sself.%s = %s\n" % (indent_block*2, device_name, device_name))
#file_out.writelines( "%sself.command_spec = %s.CommandSpec(%s)\n" % ((indent_block*2), sysex_module_name, commandspec))

methods = StringIO.StringIO()

# Commands
line = file_in.readline()
while line:
    try:
        elems = line.rstrip().split('\t')
        section_id = elems[0]
        id = elems[1]
        name = elems[2]
        desc = elems[3]

        args = ['self']
        data = []
        for i in range(4, len(elems)):
            if elems[i] != 'NA':
                data.append( sysex_types_module_name + '.' + elems[i])
                args.append('arg' + str(i-4))

        reply_spec_line = file_in.readline().rstrip().split('\t')
        #reply_spec = reply_spec_line[0:len(reply_spec_line)]
        #reply_spec_desc = reply_spec_line[len(reply_spec_line):]
        reply_spec = reply_spec_line
        args = tuple(args)

        if len(reply_spec) > 0:
            if reply_spec[0]:
                reply_spec = [ sysex_types_module_name + '.' + type for type in reply_spec ]
            else:
                reply_spec = ()


        # definition
        cmd_var_name = "self.%s_cmd" % name
        methods.writelines( "%sdef %s(%s):\n" % (indent_block, name, ', '.join(args)))
        testfile_out.writelines( "%sdef test_%s(self):\n" % (indent_block, name) )

        # docstring
        format = { 'indent': indent_block, 'desc': desc,'returns': ('\n'+indent_block*3).join(reply_spec) }
        if len(reply_spec) > 0:
            testfile_out.writelines( "%sself.%s.%s.%s()\n\n" % ((indent_block*2), device_name, section_name, name) )
            format['returns'] = "\n\n%(indent)s%(indent)sReturns:\n%(indent)s%(indent)s%(indent)s%(returns)s" % format
        else:
            testfile_out.writelines( "%sself.%s.%s()\n\n" % ((indent_block*2), device_name, name) )
            format['returns'] = ""

        methods.writelines(
            "%(indent)s%(indent)s\"\"\"%(desc)s%(returns)s\n%(indent)s%(indent)s\"\"\"\n" % format)

        # command object creation
        comm_args = []
        comm_args.extend(args[1:])
        comm_args.append('')
        methods.writelines( "%sreturn self.%s.execute(%s, %s)\n\n" % (indent_block*2, device_name, cmd_var_name, '('+ ', '.join(comm_args) + ')'))

        # put the command in a dict with tuple key (section_id, id)
        if skip_replyspec:
            replyspec_arg = None
        else:
            replyspec_arg = _arglist_helper(reply_spec)
        if userref_type is None:
            userref_type_arg = ''
        else:
            userref_type_arg = ', %s' % userref_type
        file_out.writelines(
            "%s%s = %s.Command(%s, '%s%s', '%s', %s, %s%s)\n" \
            % ((indent_block*2), cmd_var_name, sysex_module_name, repr(device_id), section_id, id, name, _arglist_helper(data), replyspec_arg, userref_type_arg))
    except IndexError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)
    except ValueError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)

    line = file_in.readline()

file_in.close()
file_out.writelines("\n%s" % methods.getvalue())
methods.close()
file_out.close()

testfile_out.writelines("""
def test_suite():
    testloader = TestLoader()
    suite = testloader.loadTestsFromName('aksy.devices.akai.%s.tests.%s')
    return suite
""" % (device_name, testfile_out_name[:-3]))

testfile_out.close()
#os.renames(destfile, os.path.join('..','tmp', 'aksy', 'devices', 'akai', device_name, destfile))
#os.renames(destfile, os.path.join('..','src', 'aksy', 'devices', 'akai', device_name, destfile))
