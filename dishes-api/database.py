import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://mongo:27017/myDatabase")

class Database:
    def __init__(self):
        self.dishes = client["db"]["dishes"]
        self.meals = client["db"]["meals"]
        self.latest_ids = client["db"]["latest_ids"]

    
    def get_dishes(self):
        return list(self.dishes.find({}, {"_id": False}))
    
    def get_meals(self):
        return list(self.meals.find({}, {"_id": False}))
    
    def delete_dish(self, id):
        self.dishes.delete_one({'_id': id})
    
    def add_dish(self, dish):
        latest_id = self.latest_ids.find_one({'collection': 'dishes'})
        if latest_id is None:
            self.latest_ids.insert_one({'collection': 'dishes', 'latest_id': 1})
            latest_id = 1
        else:
            self.latest_ids.update_one({'collection': 'dishes'}, {'$inc': {'latest_id': 1}})
            latest_id = latest_id['latest_id'] + 1
        
        dish["ID"] = latest_id
        dish["_id"] = latest_id
        result = self.dishes.insert_one(dish)
        return result.inserted_id

    def delete_meal(self, id):
        self.meals.delete_one({'_id': id})

    def add_meal(self, meal):
        latest_id = self.latest_ids.find_one({'collection': 'meals'})
        if latest_id is None:
            self.latest_ids.insert_one({'collection': 'meals', 'latest_id': 1})
            latest_id = 1
        else:
            self.latest_ids.update_one({'collection': 'meals'}, {'$inc': {'latest_id': 1}})
            latest_id = latest_id['latest_id'] + 1
        
        meal["ID"] = latest_id
        meal["_id"] = latest_id
        result = self.meals.insert_one(meal)
        
        return result.inserted_id

    def find_data_item(self, collection, target_key, target_value):
        item = collection.find_one({target_key: target_value}, {"_id": False})
        return item if item else -1