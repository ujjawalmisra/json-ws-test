import json
import re
import sys
import time
import urllib
import urllib2

from DictUtils import DictUtils
from executors.BaseExecutor import BaseExecutor
from validators.ValidatorFactory import ValidatorFactory


class TestExecutor(BaseExecutor):
    
    def __init__(self):
        TestExecutor._LOGGER.debug("created TestExecutor")
        self.__inputRE = re.compile('(\$(IN|OUT)\[([\w]+)\]\[([\w\.]+)\])')
    
    def __detemplatizeStr(self, inputStr, control):
        if None == inputStr:
            return None
        matches = self.__inputRE.findall(inputStr)
        TestExecutor._LOGGER.debug("inputStr: " + inputStr + ", matches: " + str(matches))
        tInputStr = inputStr
        
        for match in matches:
            
            paramType = match[1]
            stepId    = match[2]
            paramPath = match[3]
            
            TestExecutor._LOGGER.debug("session-steps: " + str(control['session']['steps']))
            
            if not stepId in control['session']['steps']:
                TestExecutor._LOGGER.debug("no stepId: " + stepId)
                continue
            sidObj = control['session']['steps'][stepId]
            if not paramType in sidObj:
                TestExecutor._LOGGER.debug("no paramType: " + paramType)
                continue
            sidData = sidObj[paramType]
            if None == sidData:
                TestExecutor._LOGGER.debug("no sidData")
                continue
            tokenVal = sidData
            TestExecutor._LOGGER.debug("tokenVal: " + str(tokenVal))
            for token in paramPath.split('.'):
                TestExecutor._LOGGER.debug("token: " + token)
                if token in tokenVal:
                    tokenVal = tokenVal[token]
                else:
                    tokenVal = None
                    TestExecutor._LOGGER.debug("no token found, assigned None")
                    break

            TestExecutor._LOGGER.debug("tokenVal: " + str(tokenVal))
            if None != tokenVal:
                tInputStr = tInputStr.replace(match[0], str(tokenVal))

            TestExecutor._LOGGER.debug("tInputStr: " + str(tInputStr))
        return tInputStr
    
    def __detemplatize(self, inputData, control):
        if None == inputData or not control['session']['running']:
            return inputData
        tInputData = dict()
        for k, v in inputData.iteritems():
            tV = None
            if None != v:
                if type(v) == str:
                    tV = self.__detemplatizeStr(v, control)
                elif type(v) == list:
                    tV = []
                    for item in list:
                        tV.append(TestExecutor.__detemplatizeStr(item, control))
                elif type(v) == dict:
                    tV = TestExecutor.__detemplatize(v, control)
                else:
                    tV = v
            tInputData[k] = tV
        return tInputData

    
    def __recordHit(self, control, sid, timeTaken, isPass):
        
        if not sid in control['result']['steps']:
            control['result']['steps'][sid] = {'total':{'count':0, 'time':0},
                                               'passed':{'count':0, 'time':0},
                                               'failed':{'count':0, 'time':0}}
        
        control['result']['total']['count'] += 1
        control['result']['total']['time'] += timeTaken
        
        control['result']['steps'][sid]['total']['count'] += 1
        control['result']['steps'][sid]['total']['time'] += timeTaken
        
        if isPass:
            statusKey = 'passed'
        else:
            statusKey = 'failed'
            
        control['result'][statusKey]['count'] += 1
        control['result'][statusKey]['time'] += timeTaken
        
        control['result']['steps'][sid][statusKey]['count'] += 1
        control['result']['steps'][sid][statusKey]['time'] += timeTaken
        
    
    def _execute(self, default, step, control):
        if control['loop']['running'] and 0 == control['loop']['count']:
            control['loop']['steps'].append({'step':step, 'executor':self})
        
        sid = DictUtils.defaultIfNone(step, None, 'sid')    
        if None == sid:
            TestExecutor._LOGGER.error("missing id for step: " + str(step))
            sys.exit(1)
        host = DictUtils.defaultIfNone(step, default, 'host')
        path = DictUtils.defaultIfNone(step, default, 'path')
        method = DictUtils.defaultIfNone(step, default, 'method')
        commonInputData = DictUtils.defaultIfNone(None, default, 'commonInput')
        inputData = DictUtils.defaultIfNone(step, default, 'input')
        
        if None != path:
            if path.startswith('/'):
                url = host + path
            else:
                url = host + '/' + path
        else:
            url = host
        
        url = self.__detemplatizeStr(url, control)
        TestExecutor._LOGGER.debug("url: " + url)
        
        if None == inputData:
            inputData = commonInputData
        elif None != commonInputData:
            inputData.update(commonInputData)
        
        if None != inputData:
            inputData = self.__detemplatize(inputData, control)
            data = urllib.urlencode(inputData)
        else:
            data = ""
        
        startTime = time.time()
        
        try:
            if 'POST' == method:
                res = urllib2.urlopen(url, data)
            else:
                url += "?" + data
                res = urllib2.urlopen(url)
        except IOError, e:
            TestExecutor._LOGGER.debug("caught exception e:" + str(e))
            isSuccess = False
            if hasattr(e, 'code'):
                statusCode = e.code
            else:
                statusCode = 500
            if hasattr(e, 'reason'):
                response = e.reason
            else:
                response = ""
        else:
            isSuccess = True
            statusCode = res.getcode()
            response = res.read()
        
        endTime = time.time()
        timeTaken = (endTime - startTime)
            
        TestExecutor._LOGGER.info("statusCode: " + str(statusCode))
        TestExecutor._LOGGER.info("response: " + str(response))
        
        try:
            jsonRes = json.loads(response)
            TestExecutor._LOGGER.debug("jsonRes: " + str(jsonRes))
            responseDict = DictUtils.convert(jsonRes)
            TestExecutor._LOGGER.debug("responseDict: " + str(responseDict))
        except ValueError, e:
            TestExecutor._LOGGER.debug("caught exception e:" + str(e))
            responseDict = None
        except TypeError, e:
            TestExecutor._LOGGER.debug("caught exception e:" + str(e))
            responseDict = None
        
        if control['session']['running']:
            control['session']['steps'].update({sid: {'IN':inputData, 'SC':statusCode, 'OUT':responseDict}})
            TestExecutor._LOGGER.debug("updated session: " + str(control['session'])) 
        
        if not isSuccess:
            self.__recordHit(control, sid, timeTaken, False)
            return
        
        if not 'output' in step or None == step['output']:
            self.__recordHit(control, sid, timeTaken, isSuccess)
            return
        
        statusCodeCheck = DictUtils.defaultIfNone(step, default, ['output', 'statusCode'])
        if None != statusCodeCheck and int(statusCodeCheck) != int(statusCode):
            TestExecutor._LOGGER.error("FAILED statusCodeCheck: expected=" + str(statusCodeCheck) + ", found=" + str(statusCode))
        
        if not 'params' in step['output'] or None == step['output']['params']:
            self.__recordHit(control, sid, timeTaken, isSuccess)
            return
        
        isValid = True
        for param in step['output']['params']:
            param = self.__detemplatize(param, control)
            isCheckValid = ValidatorFactory.validate(param, responseDict)
            if not isCheckValid:
                isValid = False
                break
            
        if not isValid:
            TestExecutor._LOGGER.error("VALIDATION FAILED")
        else:
            TestExecutor._LOGGER.info("VALIDATION PASSED")
        
        self.__recordHit(control, sid, timeTaken, isValid)
