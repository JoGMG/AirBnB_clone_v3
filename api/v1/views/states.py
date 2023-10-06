#!/usr/bin/python3
""" View for State objects """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states():
    if request.method == 'GET':
        all_states = [value.to_dict() for value in storage.all(State).values()]
        return jsonify(all_states)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            if 'name' not in post:
                return jsonify({"error": "Missing name"}), 400
            else:
                post_state = State(**post)
                post_state.save()
                return jsonify(post_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    state = [value.to_dict() for value in storage.all(State).values()
             if value.id == state_id]
    if request.method == 'GET':
        if len(state) == 0:
            abort(404)
        return jsonify(state[0])
    elif request.method == 'DELETE':
        if len(state) == 0:
            abort(404)
        else:
            state = storage.get(State, state_id)
            for city in list(state.cities):
                storage.delete(city)
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    elif request.method == 'PUT':
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        else:
            for key, value in post.items():
                ignore = ['id', 'created_at', 'updated_at']
                if key not in ignore:
                    state = storage.get(State, state_id)
                    setattr(state, key, value)
                    storage.save()
            return jsonify(state.to_dict()), 200
