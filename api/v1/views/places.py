#!/usr/bin/python3
""" View for User objects """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=['GET', 'POST'])
def city_places(city_id):
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city is None:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    elif request.method == 'POST':
        if city is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'user_id' not in post:
            return jsonify({"error": "Missing user_id"}), 400
        if 'name' not in post:
            return jsonify({"error": "Missing name"}), 400
        user = storage.get(User, post['user_id'])
        if user is None:
            abort(404)
        post_place = Place(**post)
        post_place.save()
        return jsonify(post_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place(place_id):
    place = storage.get(Place, place_id)
    if request.method == 'GET':
        if place is None:
            abort(404)
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        if place is None:
            abort(404)
        place.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if place is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in post.items():
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
