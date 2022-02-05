#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ Retrieve a list of cities at a given State id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = []
    for city in state.cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """ Retrieve a particular City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Delete a City """
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create a City """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # new_city = request.get_json()
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_city = request.get_json()
    new_city_obj = City(**new_city)
    new_city_obj.state_id = state.id
    new_city_obj.save()
    return jsonify(new_city_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ Update a city """
    if city_id is None:
        return abort(404)
    my_city = storage.get(City, city_id)
    if my_city is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in body.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(my_city, key, value)
        my_city.save()
        return make_response(jsonify(my_city.to_dict()), 200)
    return abort(404)
