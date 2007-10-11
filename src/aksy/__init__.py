# package aksy
import logging, logging.config, logging.handlers,  time, os.path

from config import get_config

# initialize logging
logger = logging.getLogger('aksy')
level = getattr(logging, get_config().get('logging', 'level'))
logger.setLevel(level)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s")

logdir = os.path.expanduser('~/.aksy/logs')
if not os.path.exists(logdir):
    os.makedirs(logdir)

handler = logging.FileHandler(os.path.expanduser('~/.aksy/logs/aksy_%s.log' % time.strftime("%Y%m%d")))
handler.setFormatter(formatter)

logger.addHandler(handler)
