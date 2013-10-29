import sys

from executors.BaseExecutor import BaseExecutor


class EndSessionExecutor(BaseExecutor):
    
    def __init__(self):
        EndSessionExecutor._LOGGER.debug("created EndSessionExecutor")
    
    def _execute(self, default, step, control):
        if not control['session']['running']:
            EndSessionExecutor._LOGGER.error("non-matching END_SESSION")
            sys.exit(1)
        
        if control['loop']['running'] and 0 == control['loop']['count']:
            control['loop']['steps'].append({'step':step, 'executor':self})
        
        control['session']['running'] = False
        control['session']['steps'] = {}
        EndSessionExecutor._LOGGER.debug("closed session")