#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def retrieve_reviews(place_id):
    """ retrieve all reviws at a giiven place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def jsonify_reviews_1(review_id):
    """ Function that returns a review by id """
    the_obj = storage.get(Review, review_id)
    if the_obj is None:
        abort(404)
    return jsonify(the_obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def jsonify_reviews_2(review_id):
    """ delete review by id """
    the_obj = storage.get(Review, review_id)
    if the_obj is None:
        abort(404)
    storage.delete(the_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def jsonify_reviews_3(place_id):
    """ create new review instance """
    try:
        json_post = request.get_json()
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if not json_post:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in json_post:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        if 'text' not in json_post:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        json_post['place_id'] = place_id
        user = storage.get(User, json_post['user_id'])
        if user is None:
            abort(404)
        new = Review(**json_post)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def jsonify_review_4(review_id):
    """ updates bt id """
    the_obj = storage.get(Review, review_id)
    json_put = request.get_json()
    if the_obj is None:
        abort(404)
    if not json_put:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in json_put.items():
        if key not in ['id', 'created_at', 'place_id', 'update_at', 'user_id']:
            setattr(the_obj, key, value)
    storage.save()
    return make_response(jsonify(the_obj.to_dict()), 200)
