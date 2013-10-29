import Logger
from executors.TestExecutor import TestExecutor
from executors.StartSessionExecutor import StartSessionExecutor
from executors.EndSessionExecutor import EndSessionExecutor
from executors.StartLoopExecutor import StartLoopExecutor
from executors.EndLoopExecutor import EndLoopExecutor

class ExecutorFactory:
    
    _LOGGER = Logger.getLogger('Executor')
    _LOGGER.debug("created ExecutorFactory")
    
    @staticmethod
    def getExecutor(construct):
        ExecutorFactory._LOGGER.debug("fetching executor for construct: " + construct)
        if 'TEST' == construct:
            return TestExecutor()
        elif 'START_SESSION' == construct:
            return StartSessionExecutor()
        elif 'END_SESSION' == construct:
            return EndSessionExecutor()
        elif 'START_LOOP' == construct:
            return StartLoopExecutor()
        elif 'END_LOOP' == construct:
            return EndLoopExecutor()
        else:
            return None