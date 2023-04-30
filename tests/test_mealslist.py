import unittest

from flask import Flask
from flask_restful import Api
from src.data import DataCollection
from helpers import test_helpers
import json


import app
from tests.test_app import make_dish

DISH_DATA = []
VALID_MEAL_DATA = []
INVALID_MEAL_DATA = []
ID_COUNTER = [1]


class TestMealsList(unittest.TestCase):
    
    def setUp(self):
        
        global DISH_DATA
        global VALID_MEAL_DATA
        global INVALID_MEAL_DATA
        global ID_COUNTER
        

        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
         
        INVALID_MEAL_DATA = test_helpers.invalid_meal_fixtures
        
        with open('tests/helpers/dish_fixtures.json') as json_data:
            DISH_DATA = json.load(json_data)
        
        with open('tests/helpers/valid_meal_fixtures.json') as json_data:
            VALID_MEAL_DATA = json.load(json_data)
            
        for fixture in DISH_DATA:
            make_dish(self.client, fixture)
            
    def tearDown(self) -> None:
        self.client.get('/reset_db')    
        
    def test_post_meals_valid(self):
        # Get test fixture
        meal = VALID_MEAL_DATA[0]
        
        # Send POST request
        response_post = self.client.post("/meals", json=meal)
        
        # Response status code should be 201
        self.assertEqual(response_post.status_code, 201)
        
        # Response JSON return ID of newly created meal, this ID should be ID_COUNTER
        id = response_post.json
        self.assertEqual(id, ID_COUNTER[0])
        
    
    def test_post_meals_nutrition(self):
        # Get test fixture
        meal = VALID_MEAL_DATA[1]
        
        # Send POST request, reponse returns ID of newly created dish
        response_post = self.client.post("/meals", json=meal)
        id = response_post.json
        meal["id"] = id
        
        # Test nutritional values calculations
        dish_ids = [meal["main"], meal["appetizer"], meal["dessert"]]
        nutritions = {"cal": 0, "sodium": 0, "sugar": 0}
        
        for dish_id in dish_ids:
            response_dish = self.client.get('/dishes/' + str(dish_id)).json
            nutritions["cal"] += response_dish["cal"]
            nutritions["sodium"] += response_dish["sodium"]
            nutritions["sugar"] += response_dish["sugar"]
        
        meal["cal"] = nutritions["cal"]
        meal["sugar"] = nutritions["sugar"]
        meal["sodium"] = nutritions["sodium"]
        
        # Get newly created dish
        response_get_meal_id = self.client.get("/meals/" + str(id))
        self.assertEqual(meal, response_get_meal_id.json)
        
        
    def test_post_meals_invalid_params(self):
        # Test rejection of incorrect param names
        invalid_params_name_response = self.client.post("/meals", json=INVALID_MEAL_DATA["invalid_params_name"])
        self.assertEqual(invalid_params_name_response.status_code, 422)
        self.assertEqual(invalid_params_name_response.json, -1)
        
        # Test rejection of missing params
        missing_params_response = self.client.post("/meals", json=INVALID_MEAL_DATA["missing_params"])
        self.assertEqual(missing_params_response.status_code, 422)
        self.assertEqual(missing_params_response.json, -1)
        
        # Test rejection of incorrect param types
        invalid_params_type_response = self.client.post("/meals", json=INVALID_MEAL_DATA["invalid_params_type"])
        self.assertEqual(invalid_params_type_response.status_code, 422)
        self.assertEqual(invalid_params_type_response.json, -1)
    
    
    def test_post_meals_invalid_name(self):
        # Make a valid post request
        meal = VALID_MEAL_DATA[2]
        self.client.post("/meals", json=meal)
        
        # Create new POST request with the same name
        new_meal = VALID_MEAL_DATA[0]
        new_meal["name"] = meal["name"]
        new_response_post = self.client.post("/meals", json=new_meal)
        self.assertEqual(new_response_post.status_code, 422)
        self.assertEqual(new_response_post.json, -2)
        
        
    def test_post_meals_invalid_dish_id(self):
        # Test rejection of POST requests in which one of the Dish ID's does not exist in our database
        invalid_dish_id_response = self.client.post("/meals", json=INVALID_MEAL_DATA["invalid_dish_id"])
        self.assertEqual(invalid_dish_id_response.status_code, 422)
        self.assertEqual(invalid_dish_id_response.json, -6)


if __name__ == '__main__':
    unittest.main()