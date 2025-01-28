import connexion
import uuid
from flask import Blueprint, request, jsonify

from .service import *

auth_bp = Blueprint('auth', __name__)

# Route for s'authentifier
@auth_bp.route('', methods=['POST'])
def authenticate_user_route():
    auth_data = connexion.request.get_json()
    username = auth_data.get('username')
    password = auth_data.get('password')
    token = authenticate_user(username, password)
    if token:
        response = {
            "data": {
                "token": token
            },
            "message": "OK"
        }
        return jsonify(response), 201
    else:
        return jsonify({"message": "Unauthorized"}), 401