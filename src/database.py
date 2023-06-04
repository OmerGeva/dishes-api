from flask_pymongo import PyMongo
from bson.objectid import ObjectId

mongo = PyMongo()

class Database:
    def __init__(self):
        self.dishes = mongo.db.dishes
        self.meals = mongo.db.meals
        self.diets = mongo.db.diets
    
    def get_dishes(self):
        return list(self.dishes.find())
    
    def get_meals(self):
        return list(self.meals.find())
    
    def delete_dish(self, id):
        self.dishes.delete_one({'_id': id})
    
    def add_dish(self, dish):
        document = self.dishes.find_one(sort=[("_id", -1)])

        if document is not None:
            keynum = document["_id"] + 1
        else:
            keynum = 1
            
        dish["_id"] = keynum
        result = self.dishes.insert_one(dish)
        
        return result.inserted_id

    def delete_meal(self, id):
        self.meals.delete_one({'_id': id})

    def add_meal(self, meal):
        document = self.meals.find_one(sort=[("_id", -1)])

        if document is not None:
            keynum = document["_id"] + 1
        else:
            keynum = 1
        
        meal["_id"] = keynum
        result = self.meals.insert_one(meal)
        
        return result.inserted_id

    def find_data_item(self, collection, target_key, target_value):
        item = collection.find_one({target_key: target_value})
        return item if item else -1