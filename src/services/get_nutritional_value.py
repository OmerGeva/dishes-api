import sys
sys.path.append("..")

from src.tokens import API_NINJA_KEY
import requests
from src.exceptions.ninja_exceptions import NinjaTimeoutException, NinjaEmptyException

class GetNutritionalValue():
    BASE_API_URL = "https://api.api-ninjas.com/v1/nutrition?query="

    def __init__(self, query):
        self.query = query
        
    def call(self):
        # Calculate nutrition from API-ninjas
        api_url = self.BASE_API_URL + self.query

        response = requests.get(api_url, headers={'X-Api-Key': API_NINJA_KEY})
        if response.status_code == 504:
            raise NinjaTimeoutException

        nutrition_data = response.json()
        if len(nutrition_data) == 0:
            raise NinjaEmptyException

        return self.__calculate_nutrition(nutrition_data)
        
    # private method to do the same thing from line 23 until line 30
    def __calculate_nutrition(self, nutrition_data):
        dishCal, dishSize, dishSodium, dishSugar = 0, 0, 0, 0
        for item in nutrition_data:
            dishCal += item['calories']
            dishSize += item['serving_size_g']
            dishSodium += item['sodium_mg']
            dishSugar += item['sugar_g']

        return { 'name': self.query, 'cal': dishCal, 'sodium': dishSodium, 'sugar': dishSugar }