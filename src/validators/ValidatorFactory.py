import Logger
from validators.PresentValidator import PresentValidator
from DictUtils import DictUtils
from validators.ExactValidator import ExactValidator


class ValidatorFactory:
    
    _LOGGER = Logger.getLogger('Validator')
    _LOGGER.debug("created ValidatorFactory")
    
    @staticmethod
    def getValidator(check):
        ValidatorFactory._LOGGER.debug("fetching validator for check: " + check)
        if 'PRESENT' == check:
            return PresentValidator()
        elif 'EXACT' == check:
            return ExactValidator()
        else:
            return None
    
    @staticmethod
    def validate(criteria, toValidate):
        if None == criteria:
            return True
        if not 'check' in criteria:
            return True
        validator = ValidatorFactory.getValidator(criteria['check'])
        if None == validator:
            ValidatorFactory._LOGGER.error("no validator found for check: " + criteria['check'])
            return False
        isValid = validator.validate(criteria, toValidate)
        if not isValid:
            return False
        if type(validator) == PresentValidator and 'expected' in criteria and list == type(criteria['expected']):
            for nextCriteria in criteria['expected']:
                if not 'check' in nextCriteria:
                    continue
                if not 'name' in nextCriteria:
                    ValidatorFactory._LOGGER.error("no name property found for check: " + str(nextCriteria))
                    return False
                nextToValidate = DictUtils.defaultIfNone(toValidate, None, nextCriteria['name'])
                isCheckValid = ValidatorFactory.validate(nextCriteria, nextToValidate)
                if not isCheckValid:
                    return False
        return True
