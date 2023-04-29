class DataCollection:
    def __init__(self):
        self.meal_id_counter = 0
        self.dish_id_counter = 0
        
        self.meals = {}
        self.dishes = {}
    
    def get_dishes(self):
        return self.dishes

    def get_meals(self):
        return self.meals
    
    def delete_dish(self, id):
        del self.dishes[id]

    def add_dish(self, dish):
        id = self.__generate_id('dish')
        dish['ID'] = id
        self.dishes[id] = dish
        return id
        

    def delete_meal(self, id):
        del self.meals[id]

    def add_meal(self, meal):
        id = self.__generate_id('meal')
        meal['ID'] = id
        self.meals[id] = meal
        return id
        
    # Searches for a specific data item in data. returns -1 if item doesn't exists
    def find_data_item(self, data, target_key, target_value):
        for item_key in data:
            if data[item_key][target_key] == target_value:
                return data[item_key]
            
        return -1
    
    # Generate unique ID for new data items
    def __generate_id(self, type):
        if type == 'meal':
            self.meal_id_counter += 1
            return self.meal_id_counter
        elif type == 'dish':
            self.dish_id_counter += 1
            return self.dish_id_counter

