from validators.BaseValidator import BaseValidator


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
        elif not criteria['name'] in toValidate:
            ExactValidator._LOGGER.debug("criteria['name']: " + criteria['name'] + " not in toValidate, so returning False")
            return False
        elif not 'expected' in criteria:
            ExactValidator._LOGGER.debug("no expected found in criteria, so returning True")
            return True
        else:
            if type(criteria['expected']) != type(toValidate[criteria['name']]):
                ExactValidator._LOGGER.debug("type mismatch, so returning True - type(criteria['expected']): " + str(type(criteria['expected'])) + ", type(toValidate['" + criteria['name'] + "']): " + str(type(toValidate[criteria['name']])))
                return False
            else:
                ExactValidator._LOGGER.debug("matching string criteria['expected']: " + criteria['expected'] + ", toValidate['" + criteria['name'] + "']: " + toValidate[criteria['name']])
                return criteria['expected'] == toValidate[criteria['name']]
