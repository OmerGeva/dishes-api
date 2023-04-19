class DataCollection:
    def __init__(self):
        self.meal_id_counter = 0
        self.dish_id_counter = 0
        
        self.meals = {}
        # TODO: CHANGE TO DYNAMIC
        self.dishes = {100: { 'id': 100, 'name': 'lasagna', 'cal': 1, 'sodium': 1, 'sugar': 1},
                       200: { 'id': 200, 'name': 'pizza', 'cal': 1, 'sodium': 1, 'sugar': 1},
                       3300: { 'id': 3300, 'name': 'hamburger', 'cal': 1, 'sodium': 1, 'sugar': 1}}
    
    def get_dishes(self):
        return self.dishes

    def delete_dish(self, id):
        del self.dishes[id]

    def add_dish(self, dish):
        id = dish['id']
        self.dishes[id] = dish
        return id

    def get_meals(self):
        return self.meals

    def delete_meal(self, id):
        del self.meals[id]

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

