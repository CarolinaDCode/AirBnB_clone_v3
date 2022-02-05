#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route /status on the object app_views that returns a JSON: status: OK:
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return a JSON file with Status: OK """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """ Return the number of objects in storage at a given class """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
