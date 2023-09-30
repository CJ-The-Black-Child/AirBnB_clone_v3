#!/usr/bin/python3
"""
Creates a route /status on the object app_views
"""
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    This returns a JSON response for RESTful API status.
    """
    return jsonify({"status:" "OK"})


@app_views('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Here, we retrieve the object number by type."""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        })
