#!/usr/bin/python3
"""Creates The Blueprint instance"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='api/v1')

from api.v1.views.index import *
from api.v1.states import *
from api.v1.cities import *
from api.v1.amenities import *
from api.v1.users import *
from api.v1.places import *
from api.v1.places_reviews import *
from api.v1.views.places_amenities import *
