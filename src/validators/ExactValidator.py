from validators.BaseValidator import BaseValidator


class ExactValidator(BaseValidator):
    
    def __init__(self):
        ExactValidator._LOGGER.debug("created ExactValidator")
    
    def _validate(self, criteria, toValidate):
        if None == criteria:
            return True
        elif None == toValidate:
            return False
        elif not 'name' in criteria:
            return False
        elif not criteria['name'] in toValidate:
            return False
        elif not 'expected' in criteria:
            ExactValidator._LOGGER.debug("no expected found in criteria, so returning True")
            return True
        else:
            if type(criteria['expected']) != type(toValidate[criteria['name']]):
                return False
            else:
                ExactValidator._LOGGER.debug("matching string")
                return criteria['expected'] == toValidate[criteria['name']]
            