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
ID_COUNTER = [0]


class TestMealByName(unittest.TestCase):
    
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
        
    def test_delete_meal(self):
        # Create a new meal
        response_post = self.client.post("/meals", json=VALID_MEAL_DATA[1])
        ID_COUNTER[0] += 1
        
        # Delete the newly created meal
        name = VALID_MEAL_DATA[1]["name"]
        id = response_post.json
        response_delete = self.client.delete("/meals/" + name)
        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(response_delete.json, id)
        
        # Make sure GET request returns errors
        response_get = self.client.get("/meals/" + name)
        self.assertEqual(response_get.status_code, 404)
        self.assertEqual(response_get.json, -5)
        
        # Make sure DELETE request on none existing names returns errors
        response_delete_error = self.client.delete("/meals/" + name)
        self.assertEqual(response_delete_error.status_code, 404)
        self.assertEqual(response_delete_error.json, -5)
            
            
if __name__ == '__main__':
    unittest.main()