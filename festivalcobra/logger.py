import logging

terminal_handler = logging.StreamHandler()
terminal_handler.setLevel(logging.INFO)
log_format =" %(levelname)8s| %(name)30s| %(lineno)3d|  %(message)s"
terminal_formatter = logging.Formatter(log_format)
terminal_handler.setFormatter(terminal_formatter)


def get(name): # as in __name__
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO) 
    logger.addHandler(terminal_handler)

    return logger
