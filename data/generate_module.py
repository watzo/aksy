#!/usr/bin/python
import sys, os, os.path, StringIO
import aksy.sysex

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
indent_block = "     "
sysex_module_name = 'aksy.sysex'
sampler_name = 'z48'

generate_methods = None
file_in_name = sys.argv[1]
if len(sys.argv)== 3:
    generate_methods = bool(sys.argv[2])

if len(sys.argv)== 4:
    custom_request = bool(sys.argv[3])
else:
    custom_request = False 
    
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
file_out.writelines( "%s\n" % preamble) 
file_out.writelines( "import %s\n\n" % sysex_module_name ) 
file_out.writelines( "class %s:\n" % classname_helper(section_name))
file_out.writelines( "%sdef __init__(self, z48):\n" % indent_block)
file_out.writelines( "%sself.%s = %s\n" % (indent_block*2, sampler_name, sampler_name))
file_out.writelines( "%sself.commands = {}\n" % (indent_block*2))
file_out.writelines( "%sself.command_spec = %s.CommandSpec(%s)\n" % ((indent_block*2), sysex_module_name, commandspec))

methods = StringIO.StringIO()

# Commands
line = file_in.readline()
while line:
    try:
        elems = line.rstrip().split('\t')
        section_id = elems[0]
        id = elems[1]
        if generate_methods is not None:
            elems.insert(1, method_name_helper(elems[1])) 

        name = elems[2]
        desc = elems[3]

        args = ['self']
        data = []
        for i in range(4, len(elems)):
            if elems[i] != 'NA':
                data.append( sysex_module_name + '.' + elems[i])
                args.append('arg' + str(i-4))

        reply_spec_line = file_in.readline().rstrip().split('\t')
        #reply_spec = reply_spec_line[0:len(reply_spec_line)]
        #reply_spec_desc = reply_spec_line[len(reply_spec_line):]
        reply_spec = reply_spec_line
        args = tuple(args)
            
        if len(reply_spec) > 0:
            if reply_spec[0]:
                reply_spec = [ sysex_module_name + '.' + type for type in reply_spec ]
            else:
                reply_spec = ()


        # definition
        methods.writelines( "%sdef %s(%s):\n" % (indent_block, name, ', '.join(args))) 

        # docstring
        format = { 'indent': indent_block, 'desc': desc,'returns': ('\n'+indent_block*3).join(reply_spec) }
        if len(reply_spec) > 0:
            format['returns'] = "\n\n%(indent)s%(indent)sReturns:\n%(indent)s%(indent)s%(indent)s%(returns)s" % format
        else:
            format['returns'] = ""
        
        methods.writelines(
            "%(indent)s%(indent)s\"\"\"%(desc)s%(returns)s\n%(indent)s%(indent)s\"\"\"\n" % format)
        
        # command object creation
        comm_args = []
        comm_args.extend(args[1:])
        comm_args.append('')
        methods.writelines( 
            "%scomm = self.commands.get('%s%s')\n" % (indent_block*2, section_id, id))

        if custom_request:
            extra_args = ', ' +  sysex_module_name + "." + 'AKSYS_Z48_ID'
        else: extra_args = ''
        methods.writelines( "%sreturn self.%s.execute(comm, %s%s)\n\n" % (indent_block*2, sampler_name, '('+ ', '.join(comm_args) + ')',extra_args))

        # put the command in a dict with tuple key (section_id, id) 
        file_out.writelines( 
            "%scomm = %s.Command('%s%s', '%s', %s, %s)\n" \
            % ((indent_block*2), sysex_module_name, section_id, id, name, _arglist_helper(data), _arglist_helper(reply_spec)))

        file_out.writelines("%sself.commands['%s%s'] = comm\n" % ((indent_block*2), section_id, id))
    except IndexError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)
    except ValueError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)

    line = file_in.readline()

file_in.close()
file_out.writelines("\n%s" % methods.getvalue())
methods.close()
file_out.close()
os.renames(destfile, os.path.join('..','src', 'aksy', 'devices', sampler_name, destfile))
