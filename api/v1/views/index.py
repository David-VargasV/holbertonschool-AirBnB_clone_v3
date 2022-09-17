#!/usr/bin/python
"""index file"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """return status"""
    return jsonify({'"status": "OK"'})
