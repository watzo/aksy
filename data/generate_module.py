import sys, StringIO

# could use ljust etc...
indent_block = "     "
sysex_module_name = 'sysex'
z48_instance_name = 'z48'

file_in_name = sys.argv[1]
file_in = open( file_in_name, 'r')
file_preamble = open( 'preamble', 'r')
preamble = "".join(file_preamble.readlines())
file_preamble.close() 
line = file_in.readline() 

# Section data
section_id, section_name, section_desc = line[:-1].split('\t')
file_out = open(section_name + '.py', 'w')
file_out.writelines( "\n\"\"\" Python equivalent of akai section %s\n\n%s\n\"\"\"\n\n" % (section_name,section_desc)) 
file_out.writelines( "%s\n" % preamble) 
file_out.writelines( "import %s\n" % sysex_module_name ) 

register_commands = StringIO.StringIO()
register_commands.writelines("def register_%s(%s)\n" % (section_name, z48_instance_name))

# Commands
line = file_in.readline()
while line:
    try:
        id, name, desc, data1, data2 = line[:-1].split('\t')
        reply_spec = file_in.readline()[:-1].split('\t')

        if data1 == 'NA':
            data1 = None
        else:
            data1 = sysex_module_name + '.' + data1
        if data2 == 'NA':
            data2 = None
        else:
            data2 = sysex_module_name + '.' + data2

        if data1 and data2:
            args = (z48_instance_name, 'arg1', 'arg2')
        elif data1 or data2:
            args = (z48_instance_name, 'arg')
        else:
            args = (z48_instance_name,)
            
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
            "%scomm =  %s.get(('%s','%s'))\n" \
            % (indent_block, z48_instance_name, section_id, id))

        file_out.writelines( "%sreturn %s.execute(comm, %s)\n\n" % (indent_block, z48_instance_name, '('+ ', '.join(comm_args) + ')'))

        # put the command in a dict with tuple key (section_id, id) 
        register_commands.writelines( 
            "%scomm =  %s.get(('%s','%s'), sysex.Command('%s','%s', '%s', (%s,%s), %s))\n" \
            % (indent_block, z48_instance_name, section_id, id, section_id, id, name, data1, data2, '(' + ', '.join(reply_spec) + ')'))

        register_commands.writelines("%s%s.commands[('%s', '%s')] = comm\n" % (indent_block, z48_instance_name, section_id, id))
    except ValueError, e:
        print "Parse error at line: %s, reason %s " % (line, e.args)

    line = file_in.readline()

file_in.close()
file_out.writelines(register_commands.getvalue())
register_commands.close()
file_out.close()
