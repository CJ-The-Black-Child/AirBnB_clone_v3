#!/usr/bin/python3
"""
This instantiates a new view for review objects
"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['GET'],
        strict_slashes=False)
def all_reviews(place_id):
    """
    Reviews the list of all Review objects on a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [
            review.to_dict() for review in
            storage.all(Review).values() if review.place_id == place_id
            ]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves or Get a specific review by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific review ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'],
        strict_slashes=False)
def create_review(place_id):
    """
    This creates a review for a place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    user_id = data.get('user_id')
    text = data.get('text')

    if not user_id:
        abort(400, description="Missing user_id")
    if not storage.get(User, user_id):
        abort(404, description="User not found")
    if not text:
        abort(400, description="Missing text")

    review = Review(text=text, place_id=place_id, user_id=user_id)
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in (
                "id", "created_at", "updated_at", "user_id", "place_id"
                ):
            setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
