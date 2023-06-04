from flask import jsonify, make_response

class ResponseSerializer():
    def __init__(self, data, status):
        self.data = data
        self.status = status
        
    def serialize(self):
        return make_response(jsonify(self.data), self.status)