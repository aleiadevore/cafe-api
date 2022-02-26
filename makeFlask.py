#!/usr/bin/python3
""" Basic api to access coffee shop locations and user info """
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    """ Handles methods to access user info """
    def get(self):
        """Get all users"""
        data = pd.read_csv('data/users.csv')
        data = data.to_dict() # convert data to dictionary
        return {'data': data}, 200 # return data and 200 OK code

class Locations(Resource):
    """ Handles methods to access locations """
    def get(self):
        """Get all locations"""
        data = pd.read_csv('data/locations.csv')
        data = data.to_dict()
        return {'data': data}, 200

class Welcome(Resource):
    """ Home screen, used for testing """
    def get(self):
        """ Posts welcome message, used for testing """
        return 'Hey there', 200

api.add_resource(Welcome, '/')
api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)