from flask import Flask, request
from flask_restful import Resource, Api

from data import DataCollection
from serializer import ResponseSerializer
from validators.meal_validator import MealValidator
from validators.dish_validator import DishValidator
from services.calculate_meal_nutrition import CalculateMealNutrition
from services.get_nutritional_value import GetNutritionalValue

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

col = DataCollection() 

class Dishes(Resource):
    global col

    def get(self):
        return ResponseSerializer(col.get_dishes(), 200).serialize()

    def delete(self):
        return ResponseSerializer({ }, 405).serialize()
    
    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(0, 415).serialize()
        
        req_json = request.get_json()

        validator = DishValidator(req_json, 'post').call()

        if not validator.valid:
            return ResponseSerializer(-1, 422).serialize()
        
        # Check if a dish with that name already exists
        if col.find_data_item(col.dishes, 'name', req_json['name']) != -1:
            return ResponseSerializer(-2, 422).serialize()

        dish_nutrition = GetNutritionalValue(col, req_json)
        return dish_nutrition.call()

class DishByID(Resource):
    global col
    def get(self, ID):
        dish = col.dishes.get(ID)

        if not dish:
            return ResponseSerializer(-5, 404).serialize()

        return ResponseSerializer(dish, 200).serialize()
    def delete(self, ID):
        dish = col.dishes.get(ID)

        if not dish:
            return ResponseSerializer(-5, 404).serialize()

        col.delete_dish(ID)

        return ResponseSerializer(dish['id'], 200).serialize()


class DishByName(Resource):
    global col

    def get(self, name):
        dish = col.find_data_item(col.get_dishes(), 'name', name)

        if not dish:
            return ResponseSerializer(-5, 404).serialize()

        return ResponseSerializer(dish, 200).serialize()

    def delete(self, name):
        dish = col.find_data_item(col.get_dishes(), 'name', name)

        if not dish:
            return ResponseSerializer(-5, 404).serialize()

        col.delete_dish(dish['id'])

        return ResponseSerializer(dish['id'], 200).serialize()

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
        with_nutrition = CalculateMealNutrition(col, req_json).call()
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
        validator = MealValidator(req_json, 'post').call()
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


api.add_resource(DishByName, '/dishes/<string:name>')
api.add_resource(Dishes, '/dishes')
api.add_resource(DishByID, '/dishes/<int:ID>')
api.add_resource(MealsList, '/meals')
api.add_resource(MealByID, '/meals/<int:ID>')
api.add_resource(MealByName, '/meals/<string:name>')

if __name__ == '__main__':
    print('running main.py')
    app.run(host='0.0.0.0', port=8000, debug=True)