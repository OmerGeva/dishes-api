import unittest

from flask import Flask
from flask_restful import Api
from unittest.mock import patch

from src.data import DataCollection
from src.exceptions.ninja_exceptions import NinjaEmptyException, NinjaTimeoutException
from helpers import test_helpers
import json


import app
from src.services.get_nutritional_value import GetNutritionalValue
from tests.test_app import make_dish

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
            
    def tearDown(self) -> None:
        self.client.get('/reset_db')
    
    def test_post_dishes_valid(self):
        global ID_COUNTER

        for dish in DISH_DATA:
            with patch('src.services.GetNutritionalValue.call') as mock_call:
                mock_call.return_value = {
                    'name': dish['name'],
                    'cal': 100,
                    'sodium': 200,
                    'sugar': 300
                }
                post_response = self.client.post("/dishes", json=dish)
                ID_COUNTER += 1

                self.assertEqual(post_response.status_code, 201)
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
        make_dish(self.client, dish)

        #post the identical dish again
        res = self.client.post("/dishes", json=dish)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res.json, -2)

    def test_post_dishes_apininja_invalid_dish(self):
        with patch('src.services.GetNutritionalValue.call') as mock_call:
            mock_call.side_effect = NinjaEmptyException('Ninja API returned empty response')
            res = self.client.post("/dishes", json={ 'name': 'newdish'})
            self.assertEqual(res.json, -3)



    def test_post_ninja_timeout(self):
        with patch('src.services.GetNutritionalValue.call') as mock_call:
            mock_call.side_effect = NinjaTimeoutException('Ninja API timed out')
            res = self.client.post("/dishes", json={ 'name': 'newdish'})
            self.assertEqual(res.json, -4)

