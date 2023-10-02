#!/usr/bin/python3
"""Viewing places in the storage"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, make_response, request
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns reviews of a place related by id"""
    if place_id:
        dct_place = storage.get(Place, place_id)
        if dct_place is None:
            abort(404)
        else:
            reviews = storage.all(Review).values()
            reviews_list = []
            for review in reviews:
                if review.place_id == place_id:
                    reviews_list.append(review.to_dict())
            return jsonify(reviews_list)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returns a review obj based on review id"""
    if review_id:
        dct_review = storage.get(Review, review_id)
        if dct_review is None:
            abort(404)
        else:
            return jsonify(dct_review.to_dict())


@app_views.route('reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on its id"""
    if review_id:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        else:
            storage.delete(review)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review"""
    if place_id:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()

    if "user_id" not in req:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, req['user_id'])
    if user is None:
        abort(404)

    if "text" not in req:
        return make_response(jsonify({"error": "Missing text"}), 400)
    req['place_id'] = place_id
    reviews = Review(**req)
    reviews.save()
    return make_response(jsonify(reviews.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates review information based on review id"""
    if review_id:
        review_obj = storage.get(Review, review_id)
        if review_obj is None:
            abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    for key, value in req.items():
        if key not in [
            'id',
            'user_id',
            'place_id',
            'created_at',
                'updated_at']:
            setattr(review_obj, key, value)
    review_obj.save()
    return make_response(jsonify(review_obj.to_dict()), 200)
