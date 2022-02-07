#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.state import State
from models.city import City


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def retrieve_places():
    """ retrieve all places """
    places = []
    all_places = storage.all('Place').values()
    for place in all_places:
        places.append(place.to_dict())
    return make_response(jsonify(places))


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def jsonify_places_1(city_id):
    """ Function that returns a JSON """
    the_obj = storage.get(City, city_id)
    if the_obj is None:
        abort(404)
    my_list = []
    for obj in the_obj.places:
        my_list.append(obj.to_dict())
    return jsonify(my_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def jsonify_places_2(place_id):
    the_obj = storage.get(Place, place_id)
    if the_obj:
        return jsonify(the_obj.to_dict())
    abort(404)
    
