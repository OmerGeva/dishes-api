from .base_validator import BaseValidator

class MealValidator(BaseValidator):
    REQUIRED_PARAMS = {
        'name': str, 
        'appetizer': int, 
        'main': int, 
        'dessert': int
    }