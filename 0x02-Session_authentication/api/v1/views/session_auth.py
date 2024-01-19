#!/usr/bin/env python3
""" Module of Users views
"""
from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    res.set_cookie(getenv('SESSION_NAME'), session_id)
    return res


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
