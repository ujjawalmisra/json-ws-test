import Logger

class BaseExecutor:
    
    _LOGGER = Logger.getLogger('Executor')
    
    def __init__(self):
        BaseExecutor._LOGGER.debug("created BaseExecutor")
    
    def _execute(self, default, step, control):
        pass
    
    def execute(self, default, step, control):
        BaseExecutor._LOGGER.debug("executing ...")
        BaseExecutor._LOGGER.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        self._execute(default, step, control)
        BaseExecutor._LOGGER.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        