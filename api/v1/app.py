#!/usr/bin/python3
"""
This spawns up the flask app
"""


from os import getenv
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from flask_cors import CORS
from models import storage

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """This response returns a JSON error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown(self):
    """This closes the storage session in SQLAlchemy db"""
    storage.close()


if __name__ == '__main__':
    """ This is the main function"""
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True)
