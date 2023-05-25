from flask import Flask
from flask_restful import Api

app = Flask(__name__) 
api = Api(app)

from src.routes.app import DishByName, Dishes, DishByID, MealsList, MealByID, MealByName, ResetDB

api.add_resource(DishByName, '/dishes/<string:name>')
api.add_resource(Dishes, '/dishes')
api.add_resource(DishByID, '/dishes/<int:ID>')
api.add_resource(MealsList, '/meals')
api.add_resource(MealByID, '/meals/<int:ID>')
api.add_resource(MealByName, '/meals/<string:name>')
api.add_resource(ResetDB, '/reset_db')
