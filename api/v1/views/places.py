#!/usr/bin/python3
"""
Creates the view for Place objects
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route(
        "/cities/<city_id>/places",
        methods=["GET"],
        strict_slashes=False)
def get_all_places(city_id):
    """
    Returns a list of all the places in a city
    """
    city = storage.get(city, city_id)
    if not city:
        abort(404)

    places = [
            place.to_dict() for place in storage.all(Place).values()
            if place.city_id == city_id
            ]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    This returns a place specified by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """
    DEletes a place specified by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False)
def create_place(city_id):
    """
    Creates a new place based on city id
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(404, description="Not a JSON")

    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')

    if not user_id:
        abort(400, description="Missing user_id")
    if not storage.get(User, user_id):
        abort(404, description="User not found")
    if not name:
        abort(400, description="Missing name")

    place = Place(city_id=city_id, user_id=user_id, name=name)
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a place specified by id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key in ("id", "created_at", "updated_at", "user_id", "city_id"):
            continue
        else:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict()), 200
