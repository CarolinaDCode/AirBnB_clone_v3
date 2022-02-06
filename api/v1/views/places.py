#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City


@app_views.route('/places',
                 methods=['GET'],
                 strict_slashes=False)
def retrieve_places():
    """ retrieve all places """
    places = []
    all_places = storage.all('Place').values()
    for place in all_places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_place(city_id):
    """ Retrieve a list of Place at a given City id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_place = []
    for place in city.places:
        all_place.append(place.to_dict())
    return jsonify(all_place)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """ Retrieve a particular Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete a Place """
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ create a Place """
    linked_city = storage.get("City", city_id)
    if linked_city is None:
        abort(404)
    new_place = request.get_json()
    if new_place is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_place = json.loads(input_json) -- not necessary, new_place is a dict
    if new_place.get("user_id") is None:
        return jsonify({'error': "Missing user_id"}), 400

    linked_user = storage.get("User", new_place.get("user_id"))
    if linked_user is None:
        abort(404)
    if new_place.get("name") is None:
        return jsonify({'error': "Missing name"}), 400
    new_place['city_id'] = city_id
    new_place = Place(**new_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Update a Place """
    a_place = storage.get('Place', place_id)
    if a_place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for req in request.get_json(silent=True):
        if req not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(a_place, req, request.json[req])
    a_place.save()
    return jsonify(a_place.to_dict())
