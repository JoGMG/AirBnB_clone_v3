#!/usr/bin/python3
""" View for amenity objects """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenities():
    amenities = [value.to_dict() for value in storage.all(Amenity).values()]
    if request.method == 'GET':
        return jsonify(amenities)
    elif request.method == 'POST':
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in post:
            return jsonify({"error": "Missing name"}), 400
        post_amenity = Amenity(**post)
        post_amenity.save()
        return jsonify(post_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if request.method == 'GET':
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        if amenity is None:
            abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if amenity is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in post.items():
            ignore = ['id', 'created_at', 'updated_at']
            if key not in ignore:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
