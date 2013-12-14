import argparse
import json
import pprint

import Logger
from executors.EndLoopExecutor import EndLoopExecutor
from executors.ExecutorFactory import ExecutorFactory
from DictUtils import DictUtils


class Tester:
    
    __LOGGER = Logger.getLogger('Tester')
    
    def __init__(self, configFilePath):
        Tester.__LOGGER.debug("created Tester")
        with open(configFilePath, 'r') as configFile:
            self.__config = DictUtils.convert(json.load(configFile))
        Tester.__LOGGER.debug("loaded config from: " + configFilePath)
            
    def showConfig(self):
        pprint.pprint(self.__config)
        if None != self.__config['tests']:
            for test in self.__config['tests']:
                pprint.pprint(test)
    
    def __isValidStep(self, step):
        Tester.__LOGGER.debug("validating step: " + str(step))
        return None != step and None != step['construct']
    
    def __formatResultSeparator(self):
        return "|" + ("-" * 30) + "|" + (("-" * 14 + "|") * 3)
    
    def __formatResultHead1(self):
        s = "|" + "[sid]".center(30) + "|"
        for t in ['total', 'passed', 'failed']:
            s+= ("[" + t + "]").center(14) + "|"
        return s
    
    def __formatResultHead2(self):
        s = "|" + "".ljust(30) + "|"
        i = len(['total', 'passed', 'failed'])
        while i > 0:
            s += "count".rjust(6)
            s += "avg(ms)".rjust(8)
            s += "|"
            i -= 1
        return s
    
    def __formatResultStr(self, sid, data):
        s = "|" + sid.ljust(30) + "|"
        for t in ['total', 'passed', 'failed']:
            if 0 == data[t]['count']:
                avgTime = 0
            else:
                avgTime = int(data[t]['time']*1000/data[t]['count'])
            s += str(data[t]['count']).rjust(6)
            s += str(avgTime).rjust(8)
            s += "|"
        return s
        
    def run(self):
        Tester.__LOGGER.info("in run")
        if not 'steps' in self.__config:
            Tester.__LOGGER.info("no test steps to execute")
            return
        default = DictUtils.defaultIfNone(self.__config, None, 'default')
        control = {'loop':{'running': False, 'count': 0, 'steps': []}, 
                   'session':{'running': False, 'steps': {}},
                   'result':{'total':{'count':0, 'time':0},
                             'passed':{'count':0, 'time':0},
                             'failed':{'count':0, 'time':0},
                             'steps':{}
                             }
                   }
        for step in self.__config['steps']:
            if False == self.__isValidStep(step):
                continue
            executor = ExecutorFactory.getExecutor(step['construct'])
            if None == executor:
                Tester.__LOGGER.error("no executor found for construct: " + step['construct'])
                continue
            executor.execute(default, step, control)
            if isinstance(executor, EndLoopExecutor):
                while control['loop']['running']:
                    for tStep in control['loop']['steps']:
                        tStep['executor'].execute(default, tStep['step'], control)
                    executor.execute(default, step, control)
        
        Tester.__LOGGER.info("================================")
        Tester.__LOGGER.info("[SUMMARY JSON]")
        Tester.__LOGGER.info(str(control['result']))
        Tester.__LOGGER.info("================================")
        
        Tester.__LOGGER.info("================================")
        Tester.__LOGGER.info("[SUMMARY]")
        Tester.__LOGGER.info(self.__formatResultSeparator())
        Tester.__LOGGER.info(self.__formatResultHead1())
        Tester.__LOGGER.info(self.__formatResultSeparator())
        Tester.__LOGGER.info(self.__formatResultHead2())
        Tester.__LOGGER.info(self.__formatResultSeparator())
        for step in self.__config['steps']:
            if not 'sid' in step:
                continue
            sid = step['sid']
            sidData = control['result']['steps'][sid]
            Tester.__LOGGER.info(self.__formatResultStr(sid, sidData))
        Tester.__LOGGER.info(self.__formatResultSeparator())
        Tester.__LOGGER.info(self.__formatResultStr('OVERALL', control['result']))
        Tester.__LOGGER.info(self.__formatResultSeparator())
        Tester.__LOGGER.info("================================")    


#--------------------------------
# [main]
#--------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('config', help="config file containing the tests")
args = parser.parse_args()

T = Tester(args.config)
T.run()

