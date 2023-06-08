from .base_validator import BaseValidator

class DietValidator(BaseValidator):
    REQUIRED_PARAMS = {
        'post': {
            "name" : str,
            "cal" : [int, float],
            "sodium" : [int, float],
            "sugar" : [int, float],
        }
    }