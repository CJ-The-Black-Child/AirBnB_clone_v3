#!/usr/bin/python3
"""
Creates a new view for User objects.
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.user import User

class UserView(app_views.View):
    """
    A view class for managing users.

    Attributes:
        storage: A storage object for managing users.
    """
    def __init__(self):
        self.storage = storage

    def all_users(self):
        """
        Returns a list of all users in storage.

        Returns:
            A list of users dictionaries.
        """

        users = []
        for user in self.storage.all("User").values():
            users.append(user.to_dict())

            return jsonify(users)

    def user(self, user_id):
        """
        Returns a user specified by id.

        Args:
            user_id: The id of the user to retrieve.

        Returns:
            A user dictionary.
        """

        user = self.storage.get("User", user_id)
        if not user:
            abort(404)

        return jsonify(user.to_dict())

    def delete_user(self, user_id):
        """
        Deletes a user specified by id.

        Args:
            user_id: The id of the user to deleteself.

        Returns:
            A 200 Ok response.
        """

        user = self.storage.get("User", user_id)
        if not user:
            abort(404)

        self.storage.delete(user)
        self.storage.save()

        return make_response(jsonify({}), 200)

    def add_user(self):
        """
        Creates a new user.
        
        Returns:
            A 201 Created response with the new user dictionary in the body.
        """

        if not request.get_json():
            abort(400, description="Not a JSON")

        if not request.get_json().get("email"):
            abort(400, description="Missing email")

        if not request.get_json().get("password"):
            abort(400, description="Missing password")

        user = User()
        user.email = request.get_json()["email"]
        user.password = request.get_json()["password"]
        user.save()

        return make_response(jsonify(user.to_dict()), 201)

    def update_user(self, user_id):
        """
        Updates a user specified by id.

        Args:
            user_id: The id of the user to update.

        Returns:
            A 200 OK response with the updated user dictionary in the body.
        """

        user = self.storage.get("User", user_id)
        if not user:
            abort(404)

        if not request.get_json():
            abort(400, description="Not a JSON")

        for key, value in request.get_json().items():
            if key in ("id", "created_at", "updated_at", "email"):
                continue
            else:
                setattr(user, key, value)

        self.storage.save()

        return make_response(jsonify(user.to_dict()), 200)

user_view = UserView()

app_views.add_url_rule("/users", view_func=user_view.all_users)
app_views.add_url_rule("/users/<user_id>", view_func=user_view.user)
app_views.add_url_rule("/users/<user_id>", methods=["DELETE"],
        view_func=user_view.delete_user)
app_views.add_url_rule("/users", methods=["POST"],
        view_func=user_view.add_user)
app_views.add_url_rule("/users/<user_id>", methods=["PUT"],
        views_func=user_view.update_user)
