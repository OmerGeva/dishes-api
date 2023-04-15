from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API


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
        self.meals[meal['id']] = meal
    
    # Generate ID for new datd items
    def get_id(self, type):
        if type == 'meal':
            self.meal_id_counter += 1
            return self.meal_id_counter
        elif type == 'dish':
            self.dish_id_counter += 1
            return self.dish_id_counter
    
    # Searches for a specific data item by ID
    
    # Searches for a specific data item in data. returns -1 if item doesn't exists
    def find_data_item(self, data, target_key, target_value):
        for item_key in data:
            if data[item_key][target_key] == target_value:
                return data[item_key]
            
        return -1

col = DataCollection() 

class Dishes(Resource):
    global col

    def get(self):
        return make_response(jsonify(col.get_dishes()), 200)

    def delete(self):
        return make_response({ }, 405)

# Meal classes
class MealsList(Resource):
    global col
    
    def get(self):
        return make_response(jsonify(col.get_meals()), 201)
    
    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return 0, 415
        
        req_json = request.get_json()
        
        # Check if params are specified correctly
        if not self.validate_params(req_json):
            return -1, 422
        
        # Check if a meal with that name already exists
        if col.find_data_item(col.meals, 'name', req_json['name']) != -1:
            return -2, 422
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        if not self.calculate_nutrition(req_json):
            return -6, 422
            
        # Add meal into database
        req_json['id'] = col.get_id('meal')
        col.add_meal(req_json)
        return req_json['id'], 201
    
    ####################
    # Helper Functions #
    ####################
    def validate_params(self, json):
        required_params = {'name': str, 'appetizer': int, 'main': int, 'dessert': int}
        
        # Check if json has all the neccesary keys
        if set(required_params.keys()) != set(json.keys()):
            return False
        
        # Check if values have the correct type
        for key in json:
            if type(json[key]) != required_params[key]:
                return False
        
        return True
    
    def calculate_nutrition(self, json):
        dish_ids = [json['appetizer'], json['main'], json['dessert']]
        json['cal'] = json['sodium'] = json['sugar'] = 0
        
        for id in dish_ids:
            
            # Returns 'None' if a dish with this id doesn't exist
            dish = col.dishes.get(id)
            
            if not dish:
                return False
            
            json['cal'] += dish['cal']
            json['sodium'] += dish['sodium']
            json['sugar'] += dish['sugar']

        return True
        
    

api.add_resource(Dishes, '/dishes')
api.add_resource(MealsList, '/meals')

if __name__ == '__main__':
    print('running main.py')
    app.run(host='0.0.0.0', port=8000, debug=True)