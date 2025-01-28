import connexion
from flask import Blueprint, request, jsonify
import requests

from .service import *


users_bp = Blueprint('users', __name__)


# Route pour récupérer tous les utilisateurs avec pagination
@users_bp.route('users', methods=['GET'])
def get_users_route():
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    users, total_users = get_users(page, items_per_page)

    response = {
        "message": "OK",
        "data": users,
        'pager':{
            "current": page,
            "total": (total_users + items_per_page - 1) // items_per_page
        }
    }

    return jsonify(response), 200


# Route pour récupérer un utilisateur par son ID
@users_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    # token = verify_token(connexion.request.headers.get('Authorization'))
    # if not token:
    #     return 401
    user = get_user(user_id)
    if user:
        response = {
            "message": "OK",
            "data": user
        }
        return jsonify(response), 200
    else:
        return 404


# Route pour créer un utilisateur
@users_bp.route('/user', methods=['POST'])
def create_user_route():
    user = connexion.request.get_json()
    user = create_user(user)
    if user:
        response = {
            "message": "OK",
            "data": user
        }
        return jsonify(response), 201
    else:
        return 500

# Route pour supprimer un utilisateur
@users_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    token = verify_token(connexion.request.headers.get('Authorization'))
    if not token:
        return 401
    user = delete_user(user_id)
    if user:
        response = {
            "message": "OK",
            "data": user
        }
        return jsonify(response), 204
    else:
        return 500



# Route pour modifier un utilisateur
@users_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    token = verify_token(connexion.request.headers.get('Authorization'))
    if not token:
        return  jsonify({"message": "Unauthorized"}), 401
    user = connexion.request.get_json()
    user = update_user(user_id, user)
    if user:
        response = {
            "message": "OK",
            "data": user
        }
        requests.post('http://127.0.0.1:5451/user/update/' + str(user_id))
        return jsonify(response), 200
    else:
        return jsonify({"message": "Error updating user"}), 500 