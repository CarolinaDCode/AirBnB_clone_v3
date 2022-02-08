#!/usr/bin/python3
"""
Flask web application api
"""
from flask import Flask, Blueprint, make_response
from flask_cors import CORS
from flask.json import jsonify
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """ Custom 404 response """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(param):
    """ declare a method /calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.run(host, port, threaded=True, debug=True)
