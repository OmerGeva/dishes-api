import requests
import os
import sys

#directory where file exists
current_dir = os.path.dirname(os.path.realpath(__file__))

#parent directory
parent_dir = os.path.dirname(current_dir)

#add parent directory to sys.path
sys.path.append(parent_dir)

import tokens
import serialize

class GetNutritionalValue():
    def __init__(self,  col, req_json):
        self.col = col
        self.req_json = req_json
        
    def call(self):
        # Calculate nutrition from API-ninjas
        query = self.req_json['name']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)

        response = requests.get(api_url, headers={'X-Api-Key': tokens.API_NINJA_KEY})
        if response.status_code == requests.codes.ok:
            #api-ninjas could not recognize the dish name
            if not len(response.json()):
                return ResponseSerializer(-3, 422).serialize()
            
            #calculate the required nutrition facts
            dishID = self.col.get_id('dish')
            dishName = self.req_json['name']
            dishCal, dishSize, dishSodium, dishSugar = 0, 0, 0, 0
            for item in response.json():
                dishCal += item['calories']
                dishSize += item['serving_size_g']
                dishSodium += item['sodium_mg']
                dishSugar += item['sugar_g']

            #define and add dish to col
            dish = { 'id': dishID, 'name': dishName, 'cal': dishCal, 'sodium': dishSodium, 'sugar': dishSugar}
            return ResponseSerializer(col.add_dish(dish), 201).serialize()
        #api-ninjas was not reachable
        else:
            return ResponseSerializer(-4, 504).serialize()