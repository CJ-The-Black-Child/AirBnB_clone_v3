#!/usr/bin/python3
"""Create, Read, Update, and Delete methods for city objects."""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Returns cities located in a given state identified by state_id"""
    if state_id:
        dct_state = storage.get(State, state_id)
        if dct_state is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            cities_list = []
            for city in cities:
                if city.state_id == state_id:
                    cities_list.append(city.to_dict())
            return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Returns a single city based on the given city_id"""
    if city_id:
        dct_city = storage.get(City, city_id)
        if dct_city is None:
            abort(404)
        else:
            return jsonify(dct_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city based on its city_id"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            storage.delete(city)
            storage.save()
            return make_response(({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a new city in a given state"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        if "name" not in req:
            return make_response(jsonify({"error": "Missing name"}), 400)
        req['state_id'] = state_id
        city = City(**req)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a given city"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
