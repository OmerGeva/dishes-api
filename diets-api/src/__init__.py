from flask import Flask
from flask_restful import Api

app = Flask(__name__) 
api = Api(app)

from src.routes.app import Diets, DietByName, ResetDB

api.add_resource(Diets, '/diets')
api.add_resource(DietByName, '/diets/<string:name>')
api.add_resource(ResetDB, '/reset_db')
