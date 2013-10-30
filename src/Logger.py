import logging.config
import inspect
import os


def getLogger(name):
    logger = logging.getLogger(name)
    if None == logger:
        logger = logging.getLogger('root')  
    return logger
        
srcDirPath = os.path.dirname(inspect.getfile(getLogger))
confFilePath = os.sep.join([srcDirPath, "..", "conf", "logger.conf"])
logging.config.fileConfig(confFilePath)
