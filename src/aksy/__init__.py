# package aksy
import logging, logging.config, logging.handlers,  time, os.path

# initialize logging
logger = logging.getLogger('aksy')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s")

logdir = os.path.expanduser('~/.aksy/logs')
if not os.path.exists(logdir):
    os.makedirs(logdir)

handler = logging.FileHandler(os.path.expanduser('~/.aksy/logs/aksy_%s.log' % time.strftime("%Y%m%d")))
handler.setFormatter(formatter)

logger.addHandler(handler)
