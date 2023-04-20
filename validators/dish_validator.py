from .base_validator import BaseValidator

class DishValidator(BaseValidator):
    REQUIRED_PARAMS = {
        'post': {
            "name" : str,
        }
    }