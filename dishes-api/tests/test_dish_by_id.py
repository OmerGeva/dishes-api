import unittest

from flask import Flask
from flask_restful import Api
from src.data import DataCollection
from helpers import test_helpers
import json


import app
from tests.test_app import make_dish

DISH_DATA = []

class TestDishById(unittest.TestCase):

    def setUp(self):
        global DISH_DATA

        app.app.config['TESTING'] = True
        self.client = app.app.test_client()
        
        with open('tests/helpers/dish_fixtures.json') as json_data:
            DISH_DATA = json.load(json_data)
            
    def tearDown(self) -> None:
        self.client.get('/reset_db')
    
    def test_delete_by_id(self):
        global DISH_DATA
        
        # Test all dishes in dish data 
        for dish in DISH_DATA:
            # Post a new dish to delete:
            
            post_response = make_dish(self.client, dish)
            # Delete the dish
            id_json = post_response.json

            delete_response = self.client.delete("/dishes/" + str(id_json))
            self.assertEqual(delete_response.status_code, 200)
            self.assertEqual(delete_response.json, id_json)

            # Make sure GET returns errors
            get_response = self.client.get("/dishes/" + str(id_json))
            self.assertEqual(get_response.status_code, 404)
            self.assertEqual(get_response.json, -5)

            # Make sure DELETE request on nonexistent ID returns error
            delete_error_response = self.client.delete("/dishes/" + str(id_json))
            self.assertEqual(delete_error_response.status_code, 404)
            self.assertEqual(delete_error_response.json, -5)

if __name__ == '__main__':
    unittest.main()