import logging.config


logging.config.fileConfig('../conf/logger.conf')

def getLogger(name):
    logger = logging.getLogger(name)
    if None == logger:
        logger = logging.getLogger('root')  
    return logger
      
        
