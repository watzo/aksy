from optparse import OptionParser

def create_option_parser(): 
    usage = "%prog"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", type="int", dest="port", 
          help="Port number", default=6575)
    parser.add_option("-a", dest="address", 
          help="Local address to bind/connect to", default="localhost")
    return parser
