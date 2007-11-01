import ConfigParser
import os.path, sys
from optparse import OptionParser

def create_option_parser(usage):
    parser = OptionParser(usage=usage)
    config = get_config()
    parser.add_option("-t", nargs=1, dest="sampler_type",
      help="Type of sampler (z48/mpc4k/s56k)", default=get_value(config, 'sampler', 'type'))
    parser.add_option("-c", nargs=1, dest="connector",
      help="Type of connector", default=get_value(config, 'sampler', 'connector'))

    return parser

def get_value(config, default, prop_name):
    section_override = os.path.basename(sys.argv[0])
    try:
        return config.get(section_override, prop_name)
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        return config.get(default, prop_name)

def get_config(ini_file=os.path.expanduser('~/.aksy/aksy.ini')):
    cfg = ConfigParser.ConfigParser(defaults={ 'port': '6575', 'host': 'localhost', 'basedir': os.path.expanduser('~') })
    cfg.add_section('sampler')
    cfg.set('sampler', 'type', 'z48')
    cfg.set('sampler', 'connector', 'usb')
    cfg.add_section('osc')
    cfg.add_section('osc_server')
    cfg.add_section('osc_client')
    cfg.add_section('logging')
    cfg.set('logging', 'level', 'INFO')

    cfg.read(ini_file)
    return cfg

