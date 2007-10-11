import ConfigParser
import os.path
from optparse import OptionParser


def create_option_parser(usage):
    parser = OptionParser(usage=usage)
    parser.add_option("-t", nargs=1, dest="samplerType",
      help="Type of sampler (z48/mpc4k/s56k)", default=get_config().get('sampler', 'type'))
    return parser

def get_config(ini_file=os.path.expanduser('~/.aksy/aksy.ini')):
    cfg = ConfigParser.ConfigParser(defaults={ 'port': '6575', 'host': 'localhost' })
    cfg.add_section('sampler')
    cfg.set('sampler', 'type', 'z48')
    cfg.add_section('osc')
    cfg.add_section('osc_server')
    cfg.add_section('osc_client')
    cfg.add_section('logging')
    cfg.set('logging', 'level', 'INFO')

    cfg.read(ini_file)
    return cfg

