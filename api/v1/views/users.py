#!/usr/bin/python3
"""View for User class"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, make_response, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Returns all users in the db"""
    dct_users = storage.all(User)
    users_list = []
    for value in dct_users.values():
        users_list = users_list.append(value.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def one_user(user_id):
    """Returns user object based on user_id"""
    if user_id:
        dct_users = request.get(User, user_id)
        if dct_users is None:
            abort(404)
        else:
            return jsonify(dct_users.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """deletes a user from storage based on user id"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    else:
        storage.delete(users)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new user in the storage"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "email" not in req:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in req:
        return make_response(jsonify({"error": "Missing password"}), 400)
    users = User(**req)
    users.save()
    return make_response(jsonify(users.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates user information based on their id"""
    if user_id:
        users = storage.get(User, user_id)
        if users is None:
            abort(404)
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(users, key, value)
        users.save()
        return make_response(jsonify(users.to_dict()), 200)
