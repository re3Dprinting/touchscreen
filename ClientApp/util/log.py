import logging
from constants import *
from logging.handlers import RotatingFileHandler

def dump_logger_hierarchy(note, log_to_debug):
    print(note, ": Dumping logger", log_to_debug)
    while log_to_debug is not None:
	    print("*** level: %s, name: %s, handlers: %s" % (log_to_debug.level,
							     log_to_debug.name,
							     log_to_debug.handlers))
	    log_to_debug = log_to_debug.parent

def find_root_logger():
    logger = logging.getLogger()

    if logger is None:
        return logger

    while logger.parent is not None:
        logger = logger.parent

    return logger
        
def setup_root_logger():
    # Get the root logger and set it to DEBUG level.
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # print("Octo: got logger", root_logger)
    # dump_logger_hierarchy("Octo 1", root_logger)

    # Create a rotating log handler:
    handler = RotatingFileHandler(k_logname, maxBytes=k_logmaxbytes, backupCount=k_logcount)
    handler.setLevel(logging.DEBUG)

    # Set the formatter to prefix the log message with the date, name,
    # and log level.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the root logger. We're now all set up.
    root_logger.addHandler(handler)

    return root_logger
