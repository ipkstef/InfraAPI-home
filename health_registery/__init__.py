#!/usr/bin/python
# -*- coding: utf-8 -*-
import markdown
import os
import shelve

# Import the framework

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask

app = Flask(__name__)

# Create the API - THIS IS IMPORTANT FOR YOUR ENDPOINTS TO WORK

api = Api(app)


# Connect to the DB (Using Shelve)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open('./db/devices.db')
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """Present some documentation"""

    # Open the README file

    with open(os.path.dirname(app.root_path) + '/README.md', 'r',
              encoding='utf-8') as markdown_file:

        # Read the content of the file

        content = markdown_file.read()

        # Convert to HTML

        return markdown.markdown(content)


# class holds the functions  and functions  define the methods (get/post/del)
# don't forget to initian the db function with `shelf = get_db()`

class DeviceList(Resource):

    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])  # looping over keys to put into device array

        return ({'message': 'Success', 'data': devices}, 200)

    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument('hostname', required=True)
        parser.add_argument('is-active', required=True)
        parser.add_argument('uptime', required=True)

        # parse the arguemtns into an object

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['hostname']] = args

        return ({'message': 'Database has stored Service info',
                'data': args}, 201)


# individual resource, recieve hostname as url and that will be passed to the get request

class Device(Resource):

    def get(self, hostname):
        shelf = get_db()

        # if the key does not exist in the dta stgore, return a 404 error.

        if not hostname in shelf:
            return ({'message': 'Hostname not found'}, 404)

        return ({'message': 'Hostname exists in  DB',
                'data': shelf[hostname]}, 200)

    def delete(self, hostname):
        shelf = get_db()

        if not hostname in shelf:
            return ({'message': 'Hostname not found', 'data': {}}, 404)

        del shelf[hostname]
        return ('', 204)


# Make your endping here and glue it to a class with a function to return data

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/health/<string:hostname>')
