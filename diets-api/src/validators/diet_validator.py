from .base_validator import BaseValidator

class DietValidator(BaseValidator):
    REQUIRED_PARAMS = {
        'post': {
            "name" : str,
            "cal" : int,
            "sodium" : int,
            "sugar" : int,
        }
    }