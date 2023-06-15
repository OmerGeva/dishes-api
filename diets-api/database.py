import pymongo

client = pymongo.MongoClient("mongodb://mongo:27017/")

class Database:
    def __init__(self):
        self.diets = client["db"]["diets"]
        self.latest_ids = client["db"]["latest_ids"]
    
    def get_diets(self):
        return list(self.diets.find({}, {"_id": False, "ID": False}))

    def add_diet(self, diet):
        latest_id = self.latest_ids.find_one({'collection': 'diets'})
        if latest_id is None:
            self.latest_ids.insert_one({'collection': 'diets', 'latest_id': 1})
            latest_id = 1
        else:
            self.latest_ids.update_one({'collection': 'diets'}, {'$inc': {'latest_id': 1}})
            latest_id = latest_id['latest_id'] + 1
            
        diet["ID"] = latest_id
        diet["_id"] = latest_id
        result = self.diets.insert_one(diet)
        return result.inserted_id
  
    def find_data_item(self, collection, target_key, target_value):
        item = collection.find_one({target_key: target_value}, {"_id": False, "ID": False})
        return item if item else -1