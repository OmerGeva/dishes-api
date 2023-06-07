class BaseValidator:
    def __init__(self, params, method_type):
        self.params = params
        self.method_type = method_type
        self.valid = True
        self.errors = []
        
    def call(self):        
        required = self.REQUIRED_PARAMS[self.method_type]
        diff = set(required.keys()) - set(self.params.keys())
        if len(diff) > 0:
            missing_fields = ", ".join(diff)
            self.errors.append(f"The following params are missing: {missing_fields}")
        

        incorrect_types = []
        for key in self.params:
            required_type = required.get(key)
            param_value = self.params[key]
            
            if isinstance(required_type, list):
                # Handle case where required_type is a list of types
                if not any(isinstance(param_value, t) for t in required_type):
                    incorrect_types.append(key)
            else:
                # Handle case where required_type is a single type
                if not isinstance(param_value, required_type):
                    incorrect_types.append(key)
        
        if len(incorrect_types) > 0:
            missing_fields = ", ".join(incorrect_types)
            self.errors.append(f"The following params are missing: {missing_fields}")
        
        if len(self.errors):
            self.valid = False
        
        return self