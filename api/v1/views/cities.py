#!/usr/bin/python3
""" View for State objects """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def state_cities(state_id):
    state = storage.get(State, state_id)
    if request.method == 'GET':
        if state is None:
            abort(404)
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
            return jsonify(cities)
    elif request.method == 'POST':
        if state is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in post:
            return jsonify({"error": "Missing name"}), 400
        post['state_id'] = state_id
        post_city = City(**post)
        post_city.save()
        return jsonify(post_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def cities(city_id):
    city = storage.get(City, city_id)
    if request.method == 'GET':
        if city is None:
            abort(404)
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        if city is None:
            abort(404)
        city.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if city is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in post.items():
            ignore = ['id', 'created_at', 'updated_at']
            if key not in ignore:
                setattr(city, key, value)
                storage.save()
        return jsonify(city.to_dict()), 200
