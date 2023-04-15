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
        id = meal['id']
        self.meals[id] = meal
        return id
    
    def delete_meal(self, id):
        del self.meals[id]
        
        
    # Generate ID for new datd items
    def get_id(self, type):
        if type == 'meal':
            self.meal_id_counter += 1
            return self.meal_id_counter
        elif type == 'dish':
            self.dish_id_counter += 1
            return self.dish_id_counter
    
    # Searches for a specific data item in data. returns None if item doesn't exists
    def find_data_item(self, data, target_key, target_value):
        for item_key in data:
            if data[item_key][target_key] == target_value:
                return data[item_key]
            
        return None
    
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
        return make_response(jsonify(col.get_meals()), 200)
    
    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return 0, 415
        
        req_json = request.get_json()
        
        # Check if params are specified correctly
        required_params = {'name': str, 'appetizer': int, 'main': int, 'dessert': int}
        if not col.validate_params(req_json, required_params):
            return -1, 422
        
        # Check if a meal with that name already exists
        if col.find_data_item(col.meals, 'name', req_json['name']) != None:
            return -2, 422
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        if not self.calculate_nutrition(req_json):
            return -6, 422
            
        # Add meal into database
        req_json['id'] = col.get_id('meal')
        id = col.add_meal(req_json)
        return id, 201
    
    # Replace in the future with call to NinjaAPI
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
        
class MealByID(Resource):
    global col
    
    def get(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return -5, 400

        return make_response(jsonify(meal), 200)
    
    def delete(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return -5, 400
        
        col.delete_meal(self, ID)
        return ID, 200
    
    def put(self, ID):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return 0, 415
        
        req_json = request.get_json()
        
        # Check if params are specified correctly
        required_params = {'name': str, 'appetizer': int, 'main': int, 'dessert': int, 'cal': float, 'sodium': float, 'sugar': float}
        if not col.validate_params(req_json, required_params):
            return -1, 422
        
        
        
        # Check whether we need to modify or create a new record
        meal = col.meals.get(ID)
        modify_existing_record = False if not meal else True
        
        # If we are creating a new record, we first check if a meal with that name already exists
        if not modify_existing_record and col.find_data_item(col.meals, 'name', req_json['name']) != None:
            return -2, 422
        
        # Add meal into database
        if modify_existing_record:
            req_json['id'] = ID
        else:
            req_json['id'] = col.get_id('meal')
        
        ID = col.add_meal(req_json)
        
        return ID, 201
        
    
class MealByName(Resource):
    global col
    
    def get(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if not meal:
            return -5, 400
        
        return make_response(jsonify(meal), 200)
    
    def delete(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if not meal:
            return -5, 400
        
        meal_id = meal['id']
        col.delete_meal(meal_id)
        return meal_id, 200
    

api.add_resource(Dishes, '/dishes')
api.add_resource(MealsList, '/meals')
api.add_resource(MealByID, '/meals/<int:ID>')
api.add_resource(MealByName, '/meals/<string:name>')

if __name__ == '__main__':
    print('running main.py')
    app.run(host='0.0.0.0', port=8000, debug=True)