import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://mongo:27017/myDatabase")

class Database:
    def __init__(self):
        self.dishes = client["db"]["dishes"]
        self.meals = client["db"]["meals"]
    
    def get_dishes(self):
        return list(self.dishes.find({}, {"_id": False}))
    
    def get_meals(self):
        return list(self.meals.find({}, {"_id": False}))
    
    def delete_dish(self, id):
        self.dishes.delete_one({'_id': id})
    
    def add_dish(self, dish):
        document = self.dishes.find_one(sort=[("_id", -1)])

        if document is not None:
            keynum = document["_id"] + 1
        else:
            keynum = 1
            
        dish["ID"] = keynum
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
        
        meal["ID"] = keynum
        meal["_id"] = keynum
        result = self.meals.insert_one(meal)
        
        return result.inserted_id

    def find_data_item(self, collection, target_key, target_value):
        item = collection.find_one({target_key: target_value})
        return item if item else -1