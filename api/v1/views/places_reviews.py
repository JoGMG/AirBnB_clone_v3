#!/usr/bin/python3
""" View for Place Reviews """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def place_reviews(place_id):
    place = storage.get(Place, place_id)
    if request.method == 'GET':
        if place is None:
            abort(404)
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    elif request.method == 'POST':
        if place is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'user_id' not in post:
            return jsonify({"error": "Missing user_id"}), 400
        if 'text' not in post:
            return jsonify({"error": "Missing text"}), 400
        user = storage.get(User, post['user_id'])
        if user is None:
            abort(404)
        post['place_id'] = place_id
        post_review = Review(**post)
        post_review.save()
        return jsonify(post_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    review = storage.get(Review, review_id)
    if request.method == 'GET':
        if review is None:
            abort(404)
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        if review is None:
            abort(404)
        review.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if review is None:
            abort(404)
        post = request.get_json()
        if post is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in post.items():
            ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            if key not in ignore:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
