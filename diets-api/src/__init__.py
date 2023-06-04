import sys
sys.path.append("..")

from flask import Flask
from flask_restful import Api
from database.src.database import mongo

app = Flask(__name__) 
api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"

mongo.init_app(app)

from src.routes.app import Diets, DietByName, ResetDB

api.add_resource(Diets, '/diets')
api.add_resource(DietByName, '/diets/<string:name>')
api.add_resource(ResetDB, '/reset_db')
