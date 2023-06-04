import sys
sys.path.append("..")

from flask import request
from flask_restful import Resource

from src.data import DataCollection
from src.serializer import ResponseSerializer
from src.validators.diet_validator import DietValidator
from src.constants import *

sys.path.append("..")
from database.src.database import *

col = Database()

class Diets(Resource):
    global col

    def get(self):
        return ResponseSerializer(col.get_diets(), 200).serialize()

    def post(self):
        # Only accept app/json content type
        if request.content_type != 'application/json':
            return ResponseSerializer(WRONG_REQUEST_TYPE, 415).serialize()
        
        req_json = request.get_json()

        validator = DietValidator(req_json, 'post').call()

        if not validator.valid:
            return ResponseSerializer(INVALID_PARAM, 422).serialize()
        
        # Check if a dish with that name already exists
        if col.find_data_item(col.diets, 'name', req_json['name']) != -1:
            return ResponseSerializer("Diet with name " + req_json['name'] + " already exists", 422).serialize()
    
        col.add_diet(req_json)
        
        return ResponseSerializer("Diet " + req_json['name'] + " successfully created", 201).serialize()

class DietByName(Resource):
    global col
    def get(self, name):
        diet = col.find_data_item(col.diets, 'name', name)

        if diet == -1:
            return ResponseSerializer("Diet " + name + " not found", 404).serialize()

        return ResponseSerializer(diet, 200).serialize()

# class ResetDB(Resource):
#     global col

#     def get(self):
#         col.reset_db()
#         return ResponseSerializer(1, 200).serialize()
