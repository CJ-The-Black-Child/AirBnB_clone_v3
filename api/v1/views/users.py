#!/usr/bin/python3
"""
Creates a new view for User objects.
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users')
def all_users():
    """
    Returns a list of all users in storage.

    Returns:
        A list of users dictionaries.
    """

    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>')
def user(user_id):
    """
    Returns a user specified by id.

    Args:
        user_id: The id of the user to retrieve.

    Returns:
        A user dictionary.
    """

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user specified by id.

    Args:
        user_id: The id of the user to delete.

    Returns:
        A 200 Ok response.
    """

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'])
def add_user():
    """
    Creates a new user.

    Returns:
        A 201 Created response with the new user dictionary in the body.
    """

    if not request.get_json():
        abort(400, description="Not a JSON")

    if not request.get_json().get('email'):
        abort(400, description="Missing email")

    if not request.get_json().get('password'):
        abort(400, description="Missing password")

    user = User()
    user.email = request.get_json()['email']
    user.password = request.get_json()['password']
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a user specified by id.

    Args:
        user_id: The id of the user to update.

    Returns:
        A 200 OK response with the updated user dictionary in the body.
    """

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for key, value in request.get_json().items():
        if key in ("id", "created_at", "updated_at", "email"):
            continue
        else:
            setattr(user, key, value)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
