import sys
sys.path.append("..")

from flask import request
from flask_restful import Resource

from src.data import DataCollection
from src.serializer import ResponseSerializer
from src.validators.meal_validator import MealValidator
from src.validators.dish_validator import DishValidator
from src.services.calculate_meal_nutrition import CalculateMealNutrition
from src.services.get_nutritional_value import GetNutritionalValue
from src.exceptions.ninja_exceptions import NinjaTimeoutException, NinjaEmptyException
from requests.exceptions import ConnectionError

col = DataCollection() 

class Dishes(Resource):
    global col

    def get(self):
        return ResponseSerializer(col.get_dishes(), 200).serialize()

    def delete(self):
        return ResponseSerializer({}, 405).serialize()
    
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
        
        try:
            dish_nutrition = GetNutritionalValue(req_json['name']).call()
            dish = col.add_dish(dish_nutrition)
        except NinjaTimeoutException:
            return ResponseSerializer(-4, 504).serialize()
        except ConnectionError:
            return ResponseSerializer(-4, 504).serialize()
        except NinjaEmptyException:
            return ResponseSerializer(-3, 422).serialize()
        
        return ResponseSerializer(dish, 201).serialize()

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

        if dish == -1:
            return ResponseSerializer(-5, 404).serialize()

        return ResponseSerializer(dish, 200).serialize()

    def delete(self, name):
        dish = col.find_data_item(col.get_dishes(), 'name', name)

        if dish == -1:
            return ResponseSerializer(-5, 404).serialize()

        col.delete_dish(dish['id'])

        return ResponseSerializer(dish['id'], 200).serialize()

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
        if col.find_data_item(col.meals, 'name', req_json['name']) != -1:
            return ResponseSerializer(-2, 422).serialize()
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        with_nutrition = CalculateMealNutrition(col, req_json).call()
        if len(with_nutrition) == 0:
            return ResponseSerializer(-6, 422).serialize()
            
        # Add meal into database
        id = col.add_meal(with_nutrition)
        return ResponseSerializer(id, 201).serialize()

class MealByID(Resource):
    global col
    
    def get(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return ResponseSerializer(-5, 404).serialize()

        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, ID):
        meal = col.meals.get(ID)
            
        if not meal:
            return ResponseSerializer(-5, 404).serialize()
        
        col.delete_meal(ID)
        return ResponseSerializer(ID, 200).serialize()
    
    def put(self, ID):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(0, 415).serialize()
        
        req_json = request.get_json()
        
        # Check if a meal with provided ID exists in our DB
        meal = col.meals.get(ID)
        if not meal:
            return ResponseSerializer(-5, 400).serialize()

        # Update meal fields
        updated_meal = meal
        updated_meal.update(req_json)
        
        # Check if params are specified correctly
        validator = MealValidator(updated_meal, 'post').call()
        if not validator:
            return ResponseSerializer(-1, 422).serialize()
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        with_nutrition = CalculateMealNutrition(col, updated_meal).call()
        if len(with_nutrition) == 0:
            return ResponseSerializer(-6, 422).serialize()
        
        with_nutrition['id'] = ID
        col.meals[ID] = with_nutrition
        
        
        return ResponseSerializer(ID, 200).serialize()        
    
class MealByName(Resource):
    global col
    
    def get(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if meal == -1:
            return ResponseSerializer(-5, 404).serialize()
        
        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, name):
        meal = col.find_data_item(col.get_meals(), 'name', name)
        
        # Return an error if meal doesn't exit
        if meal == -1:
            return ResponseSerializer(-5, 404).serialize()
        
        meal_id = meal['id']
        col.delete_meal(meal_id)
        return ResponseSerializer(meal_id, 200).serialize()

class ResetDB(Resource):
    global col

    def get(self):
        col.reset_db()
        return ResponseSerializer(1, 200).serialize()
