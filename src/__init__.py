from flask import Flask
from flask_restful import Api
from src.database import mongo

app = Flask(__name__) 
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo.init_app(app)

from src.routes.app import DishByName, Dishes, DishByID, MealsList, MealByID, MealByName

api.add_resource(DishByName, '/dishes/<string:name>')
api.add_resource(Dishes, '/dishes')
api.add_resource(DishByID, '/dishes/<int:ID>')
api.add_resource(MealsList, '/meals')
api.add_resource(MealByID, '/meals/<int:ID>')
api.add_resource(MealByName, '/meals/<string:name>')
# api.add_resource(ResetDB, '/reset_db')
