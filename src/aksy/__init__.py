# package aksy
# initialize logging
import logging, logging.config, logging.handlers,  time
logger = logging.getLogger('aksy')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('aksy_%s.log' % time.strftime("%Y%H%d"))
logger.addHandler(handler)