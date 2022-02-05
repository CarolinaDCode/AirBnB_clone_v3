#!/usr/bin/python3
"""
New view for State objects that handles default Restful API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Retrieve a list of all State objects """
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state(state_id):
    """ Retrieve a particular State """
    the_obj = storage.get(State, state_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete a State """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ Create a State """
    state_name = request.get_json()
    if not state_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in state_name:
        abort(400, {'Missing name'})
    new_state = State(**state_name)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Update a State """
    if state_id is None:
        return abort(404)
    my_state = storage.get(State, state_id)
    if my_state is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for key, value in body.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(my_state, key, value)
        my_state.save()
        return make_response(jsonify(my_state.to_dict()), 200)
    return abort(404)
