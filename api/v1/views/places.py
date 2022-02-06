!/usr/bin/python3
"""Places View"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    city = storage.get(City, city_id)
    if city is not None:
        if request.method == 'GET':
            places = storage.all(Place)
            new_list = []
            for key, value in places.items():
                if value.city_id == city.id:
                    new_list.append(value.to_dict())
            return jsonify(new_list)
        else:
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            if 'user_id' not in json.keys():
                abort(400, 'Missing user_id')
            if 'name' not in json.keys():
                abort(400, 'Missing name')
            user = storage.get(User, json['user_id'])
            if user is None:
                abort(404)
            json['city_id'] = city_id
            new_place = Place(**json)
            storage.new(new_place)
            storage.save()
            return jsonify(new_place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places(place_id=None):
    place = storage.get(Place, place_id)
    if place is not None:
        if request.method == 'GET':
            return jsonify(place.to_dict())
        elif request.method == 'DELETE':
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            json = request.get_json()
            if json is None:
                abort(400, 'Not a JSON')
            for key, value in json.items():
                setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict()), 200
    else:
        abort(404)
