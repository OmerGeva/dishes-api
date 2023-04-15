class DataCollection:
    def __init__(self):
        self.meal_id_counter = 0
        self.dish_id_counter = 0
        
        self.meals = {}
        # TODO: CHANGE TO DYNAMIC
        self.dishes = {1: { 'id': 1, 'name': 'lasagna', 'cal': 1, 'sodium': 1, 'sugar': 1},
                       2: { 'id': 2, 'name': 'lasagna', 'cal': 1, 'sodium': 1, 'sugar': 1},
                       3: { 'id': 3, 'name': 'lasagna', 'cal': 1, 'sodium': 1, 'sugar': 1}}
    
    def get_dishes(self):
        return self.dishes
    
    def get_meals(self):
        return self.meals
    
    def add_meal(self, meal):
        id = meal['id']
        self.meals[id] = meal
        return id
        
    # Generate ID for new datd items
    def get_id(self, type):
        if type == 'meal':
            self.meal_id_counter += 1
            return self.meal_id_counter
        elif type == 'dish':
            self.dish_id_counter += 1
            return self.dish_id_counter
    
    # Searches for a specific data item in data. returns -1 if item doesn't exists
    def find_data_item(self, data, target_key, target_value):
        for item_key in data:
            if data[item_key][target_key] == target_value:
                return data[item_key]
            
        return -1   
    
    # Checks that the parameters of the POST requests are correct
    # 'required_params' should be "name_of_key": type_of_value" pairs. E.g. {'name': str, 'id': int}
    def validate_params(self, json, required_params):
        # Check if json has all the neccesary keys
        if set(required_params.keys()) != set(json.keys()):
            return False
        
        # Check if values have the correct type
        for key in json:
            if type(json[key]) != required_params[key]:
                return False
        
        return True

