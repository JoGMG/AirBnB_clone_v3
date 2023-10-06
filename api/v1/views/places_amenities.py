#!/usr/bin/python3
""" View for Place Amenities """
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import os

storage_mode = os.getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def place_amenities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_mode == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)
    else:
        amenities = [storage.get(Amenity, ids).to_dict()
                     for ids in place.amenity_ids]
        return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if request.method == 'DELETE':
        if place is None:
            abort(404)
        if amenity is None:
            abort(404)
        if storage_mode == 'db':
            if amenity not in place.amenities:
                abort(404)
        else:
            if amenity_id not in place.amenity_ids:
                abort(404)
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    elif request.method == 'POST':
        if place is None:
            abort(404)
        if amenity is None:
            abort(404)
        if storage_mode == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                return jsonify(amenity.to_dict()), 201
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenity_ids.append(amenity_id)
                return jsonify(amenity.to_dict()), 201
