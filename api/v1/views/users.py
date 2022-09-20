#!/usr/bin/python3
"""
New view for User objects that handles
all default RESTFul API actions
"""


from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_user():
    """Retrieves the list of all user objects"""
    n_list = []
    for user in storage.all(User).values():
        n_list.append(user.to_dict())
    return jsonify(n_list)


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def one_user(user_id):
    """Deletes a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def user_delete(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """Creates a User"""
    db = request.get_json()
    if not db:
        abort(400, description="Not a JSON")
    if "email" not in db:
        abort(400, description="Missing email")
    if "password" not in db:
        abort(400, description="Misssing password")
    instance = User(**db)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    db = request.get_json()
    if not user:
        abort(404)
    if not db:
        abort(400, description="Not a JSON")

    not_keys = ['id', 'created_at', 'updated_at']

    for key, value in db.items():
        if key not in not_keys:
            setattr(user, key, value)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
