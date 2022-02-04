#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route /status on the object app_views that returns a JSON: status: OK:
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return a JSON file with Status: OK """
    return jsonify({"status": "OK"})
