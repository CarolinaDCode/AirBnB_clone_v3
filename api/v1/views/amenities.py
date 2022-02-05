#!/usr/bin/python3
"""
New view for Amenity objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """ Retrieve a list of all Amenity objects """
    all_amenity = []
    for amenity in storage.all('Amenity').values():
        all_amenity.append(amenity.to_dict())
    return jsonify(all_amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_amenity(amenity_id):
    """ Retrieve a particular amenity """
    the_obj = storage.get(Amenity, amenity_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete a Amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ Create a Amenity """
    amenity_name = request.get_json()
    if not amenity_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in amenity_name:
        abort(400, {'Missing name'})
    new_amenity = Amenity(**amenity_name)
    storage.new(new_amenity)
    storage.save()
    return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update a State """
    if amenity_id is None:
        return abort(404)
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in body.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(my_amenity, key, value)
        my_amenity.save()
        return make_response(jsonify(my_amenity.to_dict()), 200)
    return abort(404)
