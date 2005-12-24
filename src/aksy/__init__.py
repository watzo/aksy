# package aksy
# initialize logging
import logging, logging.config, logging.handlers,  time
logger = logging.getLogger('aksy')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('aksy_%s.log' % time.strftime("%Y%m%d"))
formatter = logging.Formatter(fmt="%(module)s %(lineno)d %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
