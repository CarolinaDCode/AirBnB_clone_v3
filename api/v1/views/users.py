#!/usr/bin/python3
"""
New view for user objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieve a list of all User objects """
    all_users = []
    for user in storage.all(User).values():
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user(user_id):
    """ Retrieve a particular user """
    the_obj = storage.get(User, user_id)
    if not the_obj:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Delete a user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Create a user """
    user_name = request.get_json()
    if not user_name:
        abort(400, {'Not a JSON'})
    if 'email' not in user_name:
        abort(400, {'Missing email'})
    if 'password' not in user_name:
        abort(400, {'Missing password'})
    new_user = User(**user_name)
    # storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Update a user """
    if user_id is None:
        abort(404)
    my_user = storage.get(User, user_id)
    if my_user:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in body.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(my_user, key, value)
        my_user.save()
        return make_response(jsonify(my_user.to_dict()), 200)
    return abort(404)
