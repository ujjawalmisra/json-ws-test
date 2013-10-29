from validators.BaseValidator import BaseValidator


class PresentValidator(BaseValidator):
    
    def __init__(self):
        PresentValidator._LOGGER.debug("created PresentValidator")
    
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
            PresentValidator._LOGGER.debug("no expected found in criteria, so returning True")
            return True
        else:
            if type(criteria['expected']) != type(toValidate[criteria['name']]):
                return False
            elif str == type(criteria['expected']):
                PresentValidator._LOGGER.debug("matching string")
                return criteria['expected'] == toValidate[criteria['name']]
            elif list == type(criteria['expected']):
                PresentValidator._LOGGER.debug("will match nested criteria further on")
                return True
            else:
                PresentValidator._LOGGER.debug("oops! validation failed")
                return False
