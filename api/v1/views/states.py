#!/usr/bin/python3
"""
New view for State objects that handles
all default RESTFul API actions
"""
from flask import jsonify, make_response, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False,
                 defaults={'state_id': None})
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False,)
def get_states(state_id):
    """Retrieves a State object"""
    if state_id is None:
        l_obj = []
        for x in storage.all('State').values():
            l_obj.append(x.to_dict())
        return jsonify(l_obj)
    save = storage.get(State, state_id)
    if not save:
        return make_response(jsonify({"error": "Not found"}), 404)
    return jsonify(save.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state(state_id=None):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    """Creates a State"""
    db = request.get_json(force=True, silent=True)
    if not db:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in db:
        return make_response(jsonify({"error": "Missing name"}), 400)
    x = State(**db)
    x.save()
    return make_response(jsonify(x.to_dict()), 201)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def put_state(state_id=None):
    """Updates a State object"""
    state = storage.get(State, state_id)
    db = request.get_json(force=True, silent=True)
    if not db:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    not_keys = ["id", "created_at", "updated_at"]
    if not state:
        return make_response(jsonify({"error": "Not found"}), 404)
    else:
        for key, value in db.items():
            if key not in not_keys:
                setattr(state, key, value)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
