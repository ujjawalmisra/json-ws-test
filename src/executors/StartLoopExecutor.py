import sys

from executors.BaseExecutor import BaseExecutor


class StartLoopExecutor(BaseExecutor):
    
    def __init__(self):
        StartLoopExecutor._LOGGER.debug("created StartLoopExecutor")
    
    def _execute(self, default, step, control):
        if control['loop']['running']:
            StartLoopExecutor._LOGGER.error("nested loops not supported")
            sys.exit(1)
        
        control['loop']['running'] = True
        control['loop']['count'] = 0
        control['loop']['steps'] = []
        if 'count' in step:
            control['loop']['maxCount'] = step['count']
        else:
            control['loop']['maxCount'] = 1
        StartLoopExecutor._LOGGER.debug("started loop with maxCount: " + str(control['loop']['maxCount']))