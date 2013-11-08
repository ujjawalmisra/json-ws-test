from validators.BaseValidator import BaseValidator


class PresentValidator(BaseValidator):
    
    def __init__(self):
        PresentValidator._LOGGER.debug("created PresentValidator")
    
    def _validate(self, criteria, toValidate):
        if None == criteria:
            PresentValidator._LOGGER.debug("None criteria, so returning True")
            return True
        elif None == toValidate:
            PresentValidator._LOGGER.debug("None toValidate, so returning False")
            return False
        elif not 'name' in criteria:
            PresentValidator._LOGGER.debug("'name' not in criteria, so returning False")
            return False
        elif not criteria['name'] in toValidate:
            PresentValidator._LOGGER.debug("criteria['name']: " + criteria['name'] + " not in toValidate, so returning False")
            return False
        elif not 'expected' in criteria:
            PresentValidator._LOGGER.debug("no expected found in criteria, so returning True")
            return True
        else:
            if list == type(criteria['expected']):
                PresentValidator._LOGGER.debug("will match nested criteria later")
                return True
            elif str == type(criteria['expected']):
                PresentValidator._LOGGER.debug("matching string")
                return criteria['expected'] == toValidate[criteria['name']]
            elif type(criteria['expected']) != type(toValidate[criteria['name']]):
                PresentValidator._LOGGER.debug("type mismatch criteria[expected]:" + str(type(criteria['expected'])) + ", toValidate[criteria[name]]:" + str(type(toValidate[criteria['name']])) + ", so returning False")
                return False
            else:
                PresentValidator._LOGGER.debug("oops! validation failed")
                return False
