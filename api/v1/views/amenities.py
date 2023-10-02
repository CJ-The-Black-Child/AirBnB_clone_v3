#!/usr/bin/python3
"""Handles all CRUD operations for amenity objs"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """Returns all available amenities"""
    dct_amenities = storage.all(Amenity)
    amenities_list = []
    for item in dct_amenities.values():
        amenities_list.append(item.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrives an amenity based on its id"""
    if amenity_id:
        dct_amenity = request.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        else:
            return jsonify(dct_amenity.to_dict())


def delete_amenity(amenity_id):
    """Deletes an amenity object based on its id,
    returns 404 otherwise."""
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if amenities is None:
            abort(404)
        else:
            storage.delete(amenities)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def response_amenity():
    """Creates a new amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenities = Amenity(**req)
    amenities.save()
    return make_response(jsonify(amenities.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity based on its id"""
    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)
        if amenities is None:
            abort(404)
        if not request.json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenities, key, value)
        amenities.save()
        return make_response(jsonify(amenities.to_dict()), 200)
