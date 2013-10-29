import sys

from executors.BaseExecutor import BaseExecutor


class EndLoopExecutor(BaseExecutor):
    
    def __init__(self):
        EndLoopExecutor._LOGGER.debug("created EndLoopExecutor")
    
    def _execute(self, default, step, control):
        if not control['loop']['running']:
            EndLoopExecutor._LOGGER.error("non-matching END_LOOP")
            sys.exit(1)
        
        control['loop']['count'] += 1
        EndLoopExecutor._LOGGER.debug("completed loop count: " + str(control['loop']['count']))
        
        if control['loop']['maxCount'] == control['loop']['count']:
            control['loop']['running'] = False
            control['loop']['count'] = 0
            control['loop']['steps'] = []
            EndLoopExecutor._LOGGER.debug("closed loop")
        