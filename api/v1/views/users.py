#!/usr/bin/python3
""" View for User objects """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    users = [value.to_dict() for value in storage.all(User).values()]
    if request.method == 'GET':
        return jsonify(users)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'email' not in post:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in post:
            return jsonify({"error": "Missing password"}), 400
        post_user = User(**post)
        post_user.save()
        return jsonify(post_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user(user_id):
    user = storage.get(User, user_id)
    if request.method == 'GET':
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        if user is None:
            abort(404)
        user.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if user is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in post.items():
            ignore = ['id', 'created_at', 'updated_at']
            if key not in ignore:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
