#!/usr/bin/python3
"""
New view for Place objects that handles
all default RESTFul API actions
"""


from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    n_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        n_list.append(place.to_dict())
    return jsonify(n_list)


@app_views.route("/places/<string:place_id>", strict_slashes=False)
def one_place(place_id):
    """Retrieves a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    db = request.get_json()
    if not city:
        abort(404)
    if not db:
        abort(400, description="Not a JSON")
    if "user_id" not in db:
        abort(400, description="Missing user_id")
    user = storage.get(User, db['user_id'])
    if not user:
        abort(404)
    if "name" not in db:
        abort(400, description="Missing name")
    db['city_id'] = city_id
    instance = Place(**db)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    db = request.get_json()
    if not db:
        abort(400, description="Not a JSON")
    for key, value in db.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
