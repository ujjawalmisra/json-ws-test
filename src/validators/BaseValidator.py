import Logger

class BaseValidator:
    
    _LOGGER = Logger.getLogger('Validator')
    
    def __init__(self):
        BaseValidator._LOGGER.debug("created BaseValidator")
    
    def _validate(self, criteria, toValidate):
        pass
    
    def validate(self, criteria, toValidate):
        BaseValidator._LOGGER.debug("validating ...")
        BaseValidator._LOGGER.debug("................")
        validation = self._validate(criteria, toValidate)
        BaseValidator._LOGGER.debug("................")
        return validation
        