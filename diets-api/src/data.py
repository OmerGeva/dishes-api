import sys

class DataCollection:
    
    def __init__(self):
        self.diet_id_counter = 0
        
        self.diets = {}

    def reset_db(self):
        if sys.argv[-1] != 'tests':
            return

        self.diet_id_counter = 0
        self.diets = {}

    
    def get_diets(self):
        return self.diets

    def add_diet(self, diet):
        id = self.__generate_id()
        diet['ID'] = id
        self.diets[id] = diet
        return id

    # Searches for a specific data item in data. returns -1 if item doesn't exists
    def find_data_item(self, data, target_key, target_value):
        for item_key in data:
            if data[item_key][target_key] == target_value:
                return data[item_key]
            
        return -1

    # Generate unique ID for new data items
    def __generate_id(self):
        self.diet_id_counter += 1
        return self.diet_id_counter

