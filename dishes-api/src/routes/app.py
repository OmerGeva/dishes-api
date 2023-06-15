import sys
from bson import ObjectId
sys.path.append("..")

from flask import request
from flask_restful import Resource, reqparse
from requests import Session

from src.serializer import ResponseSerializer
from src.validators.meal_validator import MealValidator
from src.validators.dish_validator import DishValidator
from src.services.calculate_meal_nutrition import CalculateMealNutrition
from src.services.get_nutritional_value import GetNutritionalValue
from src.exceptions.ninja_exceptions import NinjaTimeoutException, NinjaEmptyException
from requests.exceptions import ConnectionError
from src.constants import *

sys.path.append("..")
from database import Database

col = Database()

class Dishes(Resource):
    global col

    def get(self):
        return ResponseSerializer(col.get_dishes(), 200).serialize()

    def delete(self):
        return ResponseSerializer({}, 405).serialize()
    
    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(WRONG_REQUEST_TYPE, 415).serialize()
        
        req_json = request.get_json()

        validator = DishValidator(req_json, 'post').call()

        if not validator.valid:
            return ResponseSerializer(INVALID_PARAM, 422).serialize()
        
        # Check if a dish with that name already exists
        if col.find_data_item(col.dishes, 'name', req_json['name']) != -1:

            return ResponseSerializer(RECORD_ALREADY_EXISTS, 422).serialize()
        
        try:
            dish_nutrition = GetNutritionalValue(req_json['name']).call()
            dish = col.add_dish(dish_nutrition)
        except NinjaTimeoutException:
            return ResponseSerializer(NINJA_UNREACHABLE, 504).serialize()
        except ConnectionError:
            return ResponseSerializer(NINJA_UNREACHABLE, 504).serialize()
        except NinjaEmptyException:
            return ResponseSerializer(EMPTY_NINJA_RESPONSE, 422).serialize()
        
        return ResponseSerializer(dish, 201).serialize()

class DishByID(Resource):
    global col
    def get(self, ID):
        dish = col.find_data_item(col.dishes, 'ID', ID)

        if dish == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()

        return ResponseSerializer(dish, 200).serialize()
    
    def delete(self, ID):
        dish = col.find_data_item(col.dishes, '_id', ID)

        if dish == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()

        col.delete_dish(ID)

        return ResponseSerializer(ID, 200).serialize()

class DishByName(Resource):
    global col

    def get(self, name):
        dish = col.find_data_item(col.dishes, 'name', name)

        if dish == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()

        return ResponseSerializer(dish, 200).serialize()

    def delete(self, name):
        dish = col.find_data_item(col.dishes, 'name', name)

        if dish == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()

        col.delete_dish(dish['_id'])

        return ResponseSerializer(dish['_id'], 200).serialize()

class MealsList(Resource):
    global col
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('diet', type=str)

        args = parser.parse_args()

        #Case we weren't given a diet
        if not args['diet']:
            return ResponseSerializer(col.get_meals(), 200).serialize()

        diet = args['diet']
        api_url = 'http://diets-service:8000/diets/' + diet
        session = Session()

        response = session.get(api_url)
        
        #Case diet wasn't found
        if response.status_code == 404:
            return ResponseSerializer("Diet " + diet + " not found", 404).serialize()

        json = response.json()
        caloryCap = json['cal']
        sodiumCap = json['sodium']
        sugarCap = json['sugar']

        meals = col.get_meals().copy()

        filtered_meals = []
        for meal in meals:
            if caloryCap >= meal['cal'] and sodiumCap >= meal['sodium'] and sugarCap >= meal['sugar']:
                filtered_meals.append(meal)

        return ResponseSerializer(filtered_meals, 200).serialize()
    
    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(WRONG_REQUEST_TYPE, 415).serialize()
        
        req_json = request.get_json()

        validator = MealValidator(req_json, 'post').call()
        if not validator.valid:
            return ResponseSerializer(INVALID_PARAM, 422).serialize()
        
        # Check if a meal with that name already exists
        if col.find_data_item(col.meals, 'name', req_json['name']) != -1:
            return ResponseSerializer(RECORD_ALREADY_EXISTS, 422).serialize()
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        with_nutrition = CalculateMealNutrition(col, req_json).call()
        if len(with_nutrition) == 0:
            return ResponseSerializer(BAD_DISH_ID, 422).serialize()
            
        # Add meal into database
        id = col.add_meal(with_nutrition)
        return ResponseSerializer(id, 201).serialize()

class MealByID(Resource):
    global col
    
    def get(self, ID):
        meal = col.find_data_item(col.meals, '_id', ID)
            
        if meal == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()

        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, ID):
        meal = col.find_data_item(col.meals, "_id", ID)
        
        if meal == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()
        
        col.delete_meal(ID)
        
        return ResponseSerializer(ID, 200).serialize()
    
    def put(self, ID):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(WRONG_REQUEST_TYPE, 415).serialize()
        
        req_json = request.get_json()
        
        # Check if a meal with provided ID exists in our DB
        meal = col.find_data_item(col.meals, "_id", ID)
        if meal == -1:
            return ResponseSerializer(BAD_RECORD_ID, 400).serialize()

        # Update meal fields
        updated_meal = meal.copy()
        updated_meal.update(req_json)
        
        # Check if params are specified correctly
        validator = MealValidator(updated_meal, 'post').call()
        if not validator:
            return ResponseSerializer(INVALID_PARAM, 422).serialize()
        
        
        
        # Check if a meal with that name already exists
        meal_with_same_name = col.find_data_item(col.meals, 'name', updated_meal['name'])
        if meal_with_same_name != -1 and meal_with_same_name['ID'] != ID:
            return ResponseSerializer(-2, 422).serialize()
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        with_nutrition = CalculateMealNutrition(col, updated_meal).call()
        if len(with_nutrition) == 0:
            return ResponseSerializer(BAD_DISH_ID, 422).serialize()
        
        col.update_meal(with_nutrition, ID)

        return ResponseSerializer(ID, 200).serialize()        
    
class MealByName(Resource):
    global col
    
    def get(self, name):
        meal = col.find_data_item(col.meals, 'name', name)
        
        # Return an error if meal doesn't exit
        if meal == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()
        
        return ResponseSerializer(meal, 200).serialize()
    
    def delete(self, name):
        meal = col.find_data_item(col.meals, 'name', name)
        
        # Return an error if meal doesn't exit
        if meal == -1:
            return ResponseSerializer(BAD_RECORD_ID, 404).serialize()
        
        meal_id = meal['_id']
        col.delete_meal(meal_id)
        return ResponseSerializer(meal_id, 200).serialize()

# class ResetDB(Resource):
#     global col

#     def get(self):
#         col.reset_db()
#         return ResponseSerializer(1, 200).serialize()
