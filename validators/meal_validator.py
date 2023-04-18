from .base_validator import BaseValidator

class MealValidator(BaseValidator):
    REQUIRED_PARAMS = {
        'post': {
            'name': str, 
            'appetizer': int, 
            'main': int, 
            'dessert': int
        },
        'put': {
            'name': str, 
            'appetizer': int, 
            'main': int, 
            'dessert': int,
            'cal': float,
            'sodium': float,
            'sugar': float
        } 
    }