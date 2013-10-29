import sys

from executors.BaseExecutor import BaseExecutor


class StartSessionExecutor(BaseExecutor):
    
    def __init__(self):
        StartSessionExecutor._LOGGER.debug("created StartSessionExecutor")
    
    def _execute(self, default, step, control):
        if control['session']['running']:
            StartSessionExecutor._LOGGER.error("nested sessions not supported")
            sys.exit(1)
        
        if control['loop']['running'] and 0 == control['loop']['count']:
            control['loop']['steps'].append({'step':step, 'executor':self})
        
        control['session']['running'] = True
        control['session']['steps'] = {}
        StartSessionExecutor._LOGGER.debug("started session")