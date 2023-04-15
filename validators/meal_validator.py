class MealValidator():
    REQUIRED_PARAMS = {
        'name': str, 
        'appetizer': int, 
        'main': int, 
        'dessert': int
    }

    def __init__(self, params):
        self.params = params
        self.valid = True
        self.errors = []
        
    def call(self):        
        diff = set(self.REQUIRED_PARAMS.keys()) - set(self.params.keys())
        if len(diff) > 0:
            missing_fields = ", ".join(diff)
            self.errors.append(f"The following params are missing: {missing_fields}")
        
        incorrect_types = []
        for key in self.params:
            if type(self.params[key]) != self.REQUIRED_PARAMS.get(key):
                incorrect_types.append(key)
        if len(incorrect_types) > 0:
            missing_fields = ", ".join(incorrect_types)
            self.errors.append(f"The following params are missing: {missing_fields}")
        
        if len(self.errors):
            self.valid = False
        
        return self