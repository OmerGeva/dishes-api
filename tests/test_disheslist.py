import unittest

from flask import Flask
from flask_restful import Api
from src.data import DataCollection
from src.exceptions.ninja_exceptions import NinjaEmptyException
from helpers import test_helpers
import json


import app

DISH_DATA = []
INVALID_DISH_DATA = []
ID_COUNTER = 0

class TestDishesList(unittest.TestCase):
    
    def setUp(self):
        
        global DISH_DATA
        global INVALID_DISH_DATA

        INVALID_DISH_DATA = test_helpers.invalid_dish_fixtures

        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        with open('tests/helpers/dish_fixtures.json') as json_data:
            DISH_DATA = json.load(json_data)

    def test_post_dishes_valid(self):
        global ID_COUNTER

        #Test posting all dishes
        for dish in DISH_DATA:
            # Send POST request
            post_response = self.client.post("/dishes", json=dish)
            ID_COUNTER += 1

            # Validate status_code
            self.assertEqual(post_response.status_code, 201)

            # Validate correct ID
            self.assertEqual(post_response.json, ID_COUNTER)

    def test_post_dishes_invalid_params(self):
        global INVALID_DISH_DATA

        # Test rejection of invalid param names
        invalid_param_name_response = self.client.post("/dishes", json=INVALID_DISH_DATA['invalid_params_name'])
        self.assertEqual(invalid_param_name_response.status_code, 422)
        self.assertEqual(invalid_param_name_response.json, -1)

        # Test rejection of missing params
        missing_param_response = self.client.post("/dishes", json=INVALID_DISH_DATA["missing_params"])
        self.assertEqual(missing_param_response.status_code, 422)
        self.assertEqual(missing_param_response.json, -1)

        # Test rejection of incorrect param types
        invalid_param_type_response = self.client.post("/dishes", json=INVALID_DISH_DATA["invalid_params_type"])
        self.assertEqual(invalid_param_type_response.status_code, 422)
        self.assertEqual(invalid_param_type_response.json, -1)

    def test_post_identical_dish(self):
        dish = DISH_DATA[0]

        #post the dish to the database
        self.client.post("/dishes", json=dish)

        #post the identical dish again
        identical_post_response = self.client.post("/dishes", json=dish)
        self.assertEqual(identical_post_response.status_code, 422)
        self.assertEqual(identical_post_response.json, -2)

    def test_post_dishes_apininja_invalid_dish(self):
        global INVALID_DISH_DATA

        # Test rejection of invalid dish request to ninja-api
        with self.assertRaises(NinjaEmptyException):
            self.client.post("/dishes", json=INVALID_DISH_DATA['invalid_dish'])
