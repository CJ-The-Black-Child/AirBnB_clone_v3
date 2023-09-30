#!/usr/bin/python3
"""
This spawns up the flask app
"""


from os import getenv
from flask import Flask, make_response, jsonify
from api.vi.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """This response returns a JSON error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app/teardown_appcontext
def teardown(self):
    """This closes the storage session in SQLAlchemy db"""
    storage.close()


if __name__ == '__main__':
    """ This is the main function"""
    host_api = getenv('HBNB_API_HOST', default='0.0.0.0')
    port_api = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host_api, port=int(port_api), threaded=True)
