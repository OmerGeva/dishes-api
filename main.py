from flask import Flask, request
from flask_restful import Resource, Api

from data import DataCollection
from serializer import ResponseSerializer
from validators.meal_validator import MealValidator
from services import CalculateNutrition

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

col = DataCollection() 

class Dishes(Resource):
    global col

    def get(self):
        return ResponseSerializer(col.get_dishes(), 200).serialize()


    def delete(self):
        return ResponseSerializer({ }, 405).serialize()

# Meal classes
class MealsList(Resource):
    global col
    
    def get(self):
        return ResponseSerializer(col.get_meals(), 200).serialize()
    
    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(0, 415).serialize()
        
        req_json = request.get_json()
        
        validator = MealValidator(req_json, 'post').call()
        if not validator.valid:
            return ResponseSerializer(-1, 422).serialize()
        
        # Check if a meal with that name already exists
        if col.find_data_item(col.meals, 'name', req_json['name']) != None:
            return ResponseSerializer(-2, 422).serialize()
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        with_nutrition = CalculateNutrition(col, req_json).call()
        if len(with_nutrition) == 0:
            return ResponseSerializer(-6, 422).serialize()
            
        # Add meal into database
        with_nutrition['id'] = col.get_id('meal')
        id = col.add_meal(with_nutrition)
        return ResponseSerializer(id, 201).serialize()

        
class MealByID(Resource):
    global col
    
    def get(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return ResponseSerializer(-5, 400).serialize()

        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return ResponseSerializer(-5, 400).serialize()
        
        col.delete_meal(self, ID)
        return ResponseSerializer(ID, 200).serialize()
    
    def put(self, ID):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(0, 415).serialize()
        
        req_json = request.get_json()
        
        # Check if params are specified correctly
        validator = MealValidator(req_json, 'put').call()
        if not validator:
            return ResponseSerializer(-1, 422).serialize()
        
        # Check whether we need to modify or create a new record
        meal = col.meals.get(ID)
        modify_existing_record = False if not meal else True
        
        # If we are creating a new record, we first check if a meal with that name already exists
        if not modify_existing_record and col.find_data_item(col.meals, 'name', req_json['name']) != None:
            return ResponseSerializer(-2, 422).serialize()
        
        # Add meal into database
        if modify_existing_record:
            req_json['id'] = ID
        else:
            req_json['id'] = col.get_id('meal')
        
        ID = col.add_meal(req_json)
        
        return ResponseSerializer(ID, 201).serialize()
        
class MealByID(Resource):
    global col
    
    def get(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return ResponseSerializer(-5, 400).serialize()

        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return ResponseSerializer(-5, 400).serialize()
        
        col.delete_meal(self, ID)
        return ResponseSerializer(ID, 200).serialize()
    
    def put(self, ID):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(0, 415).serialize()
        
        req_json = request.get_json()
        
        # Check if params are specified correctly
        validator = MealValidator(req_json, 'put').call()
        if not validator:
            return ResponseSerializer(-1, 422).serialize()
        
        
        
        # Check whether we need to modify or create a new record
        meal = col.meals.get(ID)
        modify_existing_record = False if not meal else True
        
        # If we are creating a new record, we first check if a meal with that name already exists
        if not modify_existing_record and col.find_data_item(col.meals, 'name', req_json['name']) != None:
            return ResponseSerializer(-2, 422).serialize()
        
        # Add meal into database
        if modify_existing_record:
            req_json['id'] = ID
        else:
            req_json['id'] = col.get_id('meal')
        
        ID = col.add_meal(req_json)
        
        return ResponseSerializer(ID, 201).serialize()
        
    
class MealByName(Resource):
    global col
    
    def get(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if not meal:
            return ResponseSerializer(-5, 400).serialize()
        
        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if not meal:
            return ResponseSerializer(-5, 400).serialize()
        
        meal_id = meal['id']
        col.delete_meal(meal_id)
        return ResponseSerializer(meal_id, 200).serialize()
    
class MealByName(Resource):
    global col
    
    def get(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if not meal:
            return ResponseSerializer(-5, 400).serialize()
        
        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if not meal:
            return ResponseSerializer(-5, 400).serialize()
        
        meal_id = meal['id']
        col.delete_meal(meal_id)
        return ResponseSerializer(meal_id, 200).serialize()


api.add_resource(Dishes, '/dishes')
api.add_resource(MealsList, '/meals')
api.add_resource(MealByID, '/meals/<int:ID>')
api.add_resource(MealByName, '/meals/<string:name>')

if __name__ == '__main__':
    print('running main.py')
    app.run(host='0.0.0.0', port=8000, debug=True)