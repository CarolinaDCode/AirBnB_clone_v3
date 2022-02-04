#!/usr/bin/python3
"""
Flask web application api
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_db(param):
    """ declare a method /calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    app.run(host, port, threaded=True, debug=True)