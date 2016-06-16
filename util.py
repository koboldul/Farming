import logging
import logging.handlers

def get_logger(log_file_name):
	logger = logging.getLogger('apscheduler.executors.default')
	logger.setLevel(logging.INFO)
	handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="midnight", backupCount=3)
	formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger
