from flask import Flask  
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API

class DishesCollection:
    def __init__(self):
        # TODO: CHANGE TO DYNAMIC
        self.dishes = [{ "id": 1, "name": 'lasagna', 'rating': 5}, { "id": 2, 'name': 'chicken parm', 'rating': 3}]  
    def get_dishes(self):
        return self.dishes

col = DishesCollection() 

class Dishes(Resource):
    global col

    def get(self):
        return col.get_dishes(), 200

    def delete(self):
        return { }, 405



api.add_resource(Dishes, '/dishes')

if __name__ == '__main__':
    print("running main.py")
    app.run(host='0.0.0.0', port=8000, debug=True)