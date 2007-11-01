# package aksy
import logging, logging.config, logging.handlers,  time, os.path, sys

from aksy.config import get_config

# initialize logging
logger = logging.getLogger('aksy')
level = getattr(logging, get_config().get('logging', 'level'))
logger.setLevel(level)

logdir = os.path.expanduser('~/.aksy/logs')
if not os.path.exists(logdir):
    os.makedirs(logdir)

script_name = os.path.basename(sys.argv[0])
handler = logging.FileHandler(os.path.expanduser('~/.aksy/logs/%s_%s.log' % (script_name, time.strftime("%Y%m%d"))))
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
