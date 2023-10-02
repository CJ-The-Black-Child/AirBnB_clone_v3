#!/usr/bin/python3
"""Viewing places in the storage"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, make_response, request
from models.place import Place
from models.city import City
from models.user import User
import json
from os import getenv


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns places located in a specific
    city idetified by a city id"""
    if city_id:
        dct_city = storage.get(City, city_id)
        if dct_city is None:
            abort(404)
        else:
            places = storage.all(Place).values()
            places_list = []
            for place in places:
                if place.city_id == city_id:
                    places_list.append(place.to_dict())
            return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returns a place obj based on its id"""
    if place_id:
        dct_place = storage.get(Place, place_id)
        if dct_place is None:
            abort(404)
        else:
            return jsonify(dct_place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place based on its id"""
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a new place"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()

    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)

    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    req['city_id'] = city_id
    places = Place(**req)
    places.save()
    return make_response(jsonify(places.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates place information based on place id"""
    if place_id:
        places_obj = storage.get(Place, place_id)
        if places_obj is None:
            abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    for key, value in req.items():
        if key not in [
            'id',
            'user_id',
            'city_id',
            'created_at',
                'updated_at']:
            setattr(places_obj, key, value)
    places_obj.save()
    return make_response(jsonify(places_obj.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Retrives all place instances based on the request"""
    body_req = request.get_json()
    if body_req is None:
        abort(400, 'Not a JSON')

    if not body_req or (
            not body_req.get('states') and
            not body_req.get('cities') and
            not body_req.get('amenities')
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if body_req.get('states'):
        states = [storage.get("State", id) for id in body_req.get('states')]

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if body_req.get('cities'):
        cities = [storage.get("City", id) for id in body_req.get('cities')]

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if body_req.get('amenities'):
        amens = [storage.get("Amenity", id)
                 for id in body_req.get('amenities')]
        m = 0
        limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/vi/places/".format(port)
        while m < limit:
            place = places[m]
            url = "{}/amenities".format(first_url, place.id)
            req = url.format(place.id)
            response = requests.get(req)
            amen_dct = json.loads(response.text)
            amenities = [storage.get("Amenity", k['id']) for k in amen_dct]
            for amenity in amens:
                if amenity not in amenities:
                    places.pop(m)
                    m -= 1
                    limit -= 1
                    break
            m += 1
    return jsonify([place.to_dict() for place in places])
