import logging
import logging.handlers
from mailer import Mailer

class Notifier:
    LOG_FILE ='farming.log'

    def __init__(self):
        self._logger = self.get_logger(Notifier.LOG_FILE)
        self._mailer = Mailer()

    def get_logger(self, log_file_name):
	    logger = logging.getLogger('apscheduler.executors.default')
	    logger.setLevel(logging.INFO)
	    handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="midnight", backupCount=3)
	    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
	    handler.setFormatter(formatter)
	    logger.addHandler(handler)
	    return logger
    
    #Will log the message and will send a mail
    def notify(self, message, digest):
        print message
        self._logger.info(message)
        self._mailer.send_message(message, digest) 

    def log(self, message):
        print message
        self._logger.info(message)
