#!/usr/bin/python
# -*- coding: utf-8 -*-
import markdown
import os
import shelve

# Import the framework

from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api, reqparse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

# Create an instance of Flask

app = Flask(__name__)

# Setup default limiter

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["300 per hour"]
)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = '1phZsRQn3u6pn50XBEPEwQ9v7tYMd7SykesaMxRbqevsgXNaLGi3boJQpCY0EZ1'  # Change this!  # Change this!
jwt = JWTManager(app)

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





# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'stef' or password != 'yezolove101':
        return jsonify({"msg": "Bad username or password"}), 401
 


    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 20

@app.route('/devices', methods=['GET'])
@limiter.limit("120 per hour")
def devices():
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])  # looping over keys to put into device array

        return ({'message': 'Success', 'data': devices}, 200)


@app.route('/devices', methods=['POST'])
@jwt_required
@limiter.exempt # exemtipn from the default limit because this has auth
def post():

        parser = reqparse.RequestParser()

        parser.add_argument('hostname', required=True)
        parser.add_argument('Containers-active', required=True)
        parser.add_argument('uptime', required=True)
        parser.add_argument('date', required=True)

        # parse the arguemtns into an object

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['hostname']] = args

        return ({'message': 'Database has stored Service info','data': args}, 201)

  
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
api.add_resource(Device, '/health/<string:hostname>')







# @app.route('/')
# def index():
#     """Present some documentation"""

#     # Open the README file

#     with open(os.path.dirname(app.root_path) + '/README.md', 'r',
#               encoding='utf-8') as markdown_file:

#         # Read the content of the file

#         content = markdown_file.read()

#         # Convert to HTML

#         return markdown.markdown(content)


# class holds the functions  and functions  define the methods (get/post/del)
# don't forget to initian the db function with `shelf = get_db()`

# class DeviceList(Resource):







# Make your endping here and glue it to a class with a function to return data

#api.add_resource(DeviceList, '/devices')

