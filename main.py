from flask import Flask, request
from flask_restful import Resource, Api

from data import DataCollection
from serializer import ResponseSerializer
from validators.meal_validator import MealValidator
from services import CalculateNutrition

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

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
            return 0, 415
        
        req_json = request.get_json()
        
        validator = MealValidator(req_json).call()
        if not validator.valid:
            return -1, 422
        
        # Check if a meal with that name already exists
        if col.find_data_item(col.meals, 'name', req_json['name']) != -1:
            return -2, 422
        
        # Calculate the total nutrition of the dishes, returns error if a dish doesn't exist
        with_nutrition = CalculateNutrition(col, req_json).call()
        if len(with_nutrition) == 0:
            return -6, 422
            
        # Add meal into database
        with_nutrition['id'] = col.get_id('meal')
        id = col.add_meal(with_nutrition)
        return ResponseSerializer(id, 201).serialize()

api.add_resource(Dishes, '/dishes')
api.add_resource(MealsList, '/meals')

if __name__ == '__main__':
    print('running main.py')
    app.run(host='0.0.0.0', port=8000, debug=True)