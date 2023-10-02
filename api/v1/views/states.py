#!/usr/bin/python3
"""End point that handles all default RESTFul api actions for states"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all state objects"""
    dct_states = storage.all(State)
    states = []
    for state in dct_states.values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    """Returns a json representation of a state
    or 404 if the state does not exist"""
    if state_id:
        dct_state = storage.get(State, state_id)
        if dct_state is None:
            abort(404)
        else:
            return jsonify(dct_state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state obj based on its id."""
    if state_id:
        state_obj = storage.get(State, state_id)
        if state_obj is None:
            abort(404)
        else:
            storage.delete(state_obj)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new state obj or raises error 400 if
    HTTP body is not a valid json"""
    if not request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**req)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates attributes of a state object"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
