#!/usr/bin/python3
"""
New view for City objects that handles
all default RESTFul API actions
"""


from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    l_cities = []
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    for city in state.cities:
        l_cities.append(city.to_dict())
    return jsonify(l_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city(city_id=None):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["POST"])
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    db = request.get_json(force=True, silent=True)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    if not db:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in db:
        return make_response(jsonify({"error": "Missing name"}), 400)
    x = City(**db)
    x.state_id = state.id
    x.save()
    return make_response(jsonify(x.to_dict()), 201)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id=None):
    """Updates a City object"""
    city = storage.get(City, city_id)
    db = request.get_json(force=True, silent=True)
    if not db:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    not_keys = ["id", "state_id", "created_at", "updated_at"]
    if not city:
        return make_response(jsonify({"error": "Not found"}), 404)
    else:
        for key, value in db.items():
            if key not in not_keys:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
