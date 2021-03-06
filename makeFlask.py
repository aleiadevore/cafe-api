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
        """ Get all users """
        data = pd.read_csv('data/users.csv')
        data = data.to_dict()  # convert data to dictionary
        return {'data': data}, 200  # return data and 200 OK code

    def post(self):
        """ Creates new user """
        parser = reqparse.RequestParser()  # initialize parser

        # Add arguments
        parser.add_argument('userId', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('city', required=True)

        # Parse arguments into a dictionary
        args = parser.parse_args()

        """Create pandas dataframe:
        a two-dimensional, size-mutable,
        potentially heterogeneous tabular data"""
        new_data = pd. DataFrame({
            'userId': args['userId'],
            'name': args['name'],
            'city': args['city'],
            'locations': [[]]
        })

        # Read csv
        data = pd.read_csv('data/users.csv')
        # Check if user already exists
        if args['userId'] in list(data['userId']):
            return {
                'message': f"'{args['userId']}' already exists."
            }, 401
        # Add new values
        data = data.append(new_data, ignore_index=True)
        # Save back to csv
        data.to_csv('data/users.csv', index=False)

        # Return new data set with 200 OK status
        return {'data': data.to_dict()}, 200

    def put(self):
        """ Adds a location to a user """
        parser = reqparse.RequestParser()  # initialize parser

        # Add arguments
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dict

        # read csv
        data = pd.read_csv('data/users.csv')

        # Check if user exists
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['locations'] = data['locations'].apply(
                # ast.literal_eval safely evaluates strings
                lambda x: ast.literal_eval(x)
            )
            # select user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])

            # save back to csv
            data.to_csv('data/users.csv', index=False)

            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # If user doesn't exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404

    def delete(self):
        """ Deletes user """
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('userId', required=True)
        args = parser.parse_args()

        # read csv
        data = pd.read_csv('data/users.csv')

        if args['userId'] in list(data['userId']):
            # If user found
            user = data[data['userId'] == args['userId']]
            # remove data entry matching userId
            data = data[data['userId'] != args['userId']]
            data.to_csv('data/users.csv', index=False)
            return {'data': data.to_dict()}, 200
        else:
            # If user not found
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404


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
