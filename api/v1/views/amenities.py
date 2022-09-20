#!/usr/bin/python3
"""
New view for Amenity objects that handles
all default RESTFul API actions
"""


from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
def get_amenity():
    """Retrieves the list of all Amenity objects"""
    n_list = []
    for amenity in storage.all(Amenity).values():
        n_list.append(amenity.to_dict())
    return jsonify(n_list)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False)
def one_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """Creates a Amenity"""
    db = request.get_json()
    if not db:
        abort(400, description="Not a JSON")
    if "name" not in db:
        abort(400, description="Missing name")
    instance = Amenity(**db)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    db = request.get_json()
    if not amenity:
        abort(404)
    if not db:
        abort(400, description="Not a JSON")

    not_key = ['id', 'created_at', 'updated_at']

    for key, value in db.items():
        if key not in not_key:
            setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
