import sys, os, StringIO
import sysex

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

# could use ljust etc...
indent_block = "     "
sysex_module_name = 'sysex'
z48_instance_name = 'z48'

generate_methods = None
file_in_name = sys.argv[1]
if len(sys.argv)== 3:
    generate_methods = sys.argv[2]
    
file_in = open( file_in_name, 'r')
file_preamble = open( 'preamble', 'r')
preamble = "".join(file_preamble.readlines())
file_preamble.close() 
line = file_in.readline() 

# Section data
section_id, section_name, section_desc = line[:-1].split('\t')
destfile = section_name + '.py'
file_out = open(destfile, 'w')
file_out.writelines( "\n\"\"\" Python equivalent of akai section %s\n\n%s\n\"\"\"\n\n" % (section_name,section_desc)) 
file_out.writelines( "%s\n" % preamble) 
file_out.writelines( "import %s\n" % sysex_module_name ) 

register_commands = StringIO.StringIO()
register_commands.writelines("def register_%s(%s):\n" % (section_name, z48_instance_name))

# Commands
line = file_in.readline()
while line:
    try:
        elems = line[:-1].split('\t')
        id = elems[0]
        if generate_methods is not None:
            elems.insert(1, method_name_helper(elems[1])) 

        name = elems[1]
        desc = elems[2]

        args = []
        data = []
        for i in range(3, len(elems)-1):
            if elems[i] != 'NA':
                data.append( sysex_module_name + '.' + elems[i])
                args.append('arg' + str(i-3))

        reply_spec_line = file_in.readline()[:-1].split('\t')
        #reply_spec = reply_spec_line[0:len(reply_spec_line)]
        #reply_spec_desc = reply_spec_line[len(reply_spec_line):]
        reply_spec = reply_spec_line
        args.insert(0, z48_instance_name)
        args = tuple(args)
            
        if len(reply_spec) > 0:
            if reply_spec[0]:
                reply_spec = [ sysex_module_name + '.' + type for type in reply_spec ]
            else:
                reply_spec = ()


        # definition
        file_out.writelines( "def %s(%s):\n" % (name, ', '.join(args))) 

        # docstring
        format = { 'indent': indent_block, 'desc': desc, 'returns': ('\n'+indent_block*2).join(reply_spec) }
        file_out.writelines( "%(indent)s\"\"\"%(desc)s\n\n%(indent)sReturns:\n%(indent)s%(indent)s%(returns)s%(indent)s\n%(indent)s\"\"\"\n" % format)
        
        # command object creation
        comm_args = []
        comm_args.extend(args[1:])
        comm_args.append('')
        file_out.writelines( 
            "%scomm =  %s.commands.get(('%s','%s'))\n" \
            % (indent_block, z48_instance_name, section_id, id))

        file_out.writelines( "%sreturn %s.execute(comm, %s)\n\n" % (indent_block, z48_instance_name, '('+ ', '.join(comm_args) + ')'))

        # put the command in a dict with tuple key (section_id, id) 
        register_commands.writelines( 
            "%scomm = sysex.Command('%s','%s', '%s', %s, %s)\n" \
            % (indent_block, section_id, id, name, _arglist_helper(data), _arglist_helper(reply_spec)))

        register_commands.writelines("%s%s.commands[('%s', '%s')] = comm\n" % (indent_block, z48_instance_name, section_id, id))
    except IndexError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)
    except ValueError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)

    line = file_in.readline()

file_in.close()
file_out.writelines(register_commands.getvalue())
register_commands.close()
file_out.close()
os.renames(destfile, '../src/' + destfile) 
