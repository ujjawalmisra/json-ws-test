from validators.BaseValidator import BaseValidator
from DictUtils import DictUtils


class ExactValidator(BaseValidator):
    
    def __init__(self):
        ExactValidator._LOGGER.debug("created ExactValidator")
    
    def _validate(self, criteria, toValidate):
        if None == criteria:
            ExactValidator._LOGGER.debug("None criteria, so returning True")
            return True
        elif None == toValidate:
            ExactValidator._LOGGER.debug("None toValidate, so returning False")
            return False
        elif not 'name' in criteria:
            ExactValidator._LOGGER.debug("'name' not in criteria, so returning False")
            return False
        elif None == DictUtils.defaultIfNone(toValidate, None, criteria['name']):
            ExactValidator._LOGGER.debug("criteria['name']: " + criteria['name'] + " not in toValidate, so returning False")
            return False
        elif not 'expected' in criteria:
            ExactValidator._LOGGER.debug("no expected found in criteria, so returning True")
            return True
        else:
            toValidateVal = DictUtils.defaultIfNone(toValidate, None, criteria['name'])
            if type(criteria['expected']) != type(toValidateVal):
                ExactValidator._LOGGER.debug("type mismatch, so returning True - type(criteria['expected']): " + str(type(criteria['expected'])) + ", type(toValidate['" + criteria['name'] + "']): " + str(type(toValidateVal)))
                return False
            else:
                ExactValidator._LOGGER.debug("matching string criteria['expected']: " + criteria['expected'] + ", toValidate['" + criteria['name'] + "']: " + toValidateVal)
                return criteria['expected'] == toValidateVal
