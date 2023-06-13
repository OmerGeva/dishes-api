import pymongo

client = pymongo.MongoClient("mongodb://mongo:27017/")

class Database:
    def __init__(self):
        self.diets = client["db"]["diets"]
    
    def get_diets(self):
        # self.diets.drop()

        return list(self.diets.find({}, {"_id": False, "ID": False}))

    def add_diet(self, diet):
        document = self.diets.find_one(sort=[("_id", -1)])

        if document is not None:
            keynum = document["_id"] + 1
        else:
            keynum = 1
            
        diet["ID"] = keynum
        diet["_id"] = keynum
        result = self.diets.insert_one(diet)
        return result.inserted_id
  
    def find_data_item(self, collection, target_key, target_value):
        item = collection.find_one({target_key: target_value})
        return item if item else -1