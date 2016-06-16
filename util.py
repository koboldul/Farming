import logging
import logging.handlers

def get_logger(log_filen_ame):
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=3)
	formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

