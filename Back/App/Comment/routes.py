import connexion
from flask import Blueprint, request, jsonify

from .service import *

comment_bp = Blueprint('/video/<int:id>/comment', __name__)


# Route pour enregistrer un commentaire pour une vidéo spécifique
@comment_bp.route('/video/<int:video_id>/comment', methods=['POST'])
def create_comment_route(video_id):
    comment_data = connexion.request.get_json()
    comment_data['video_id'] = video_id
    comment = create_comment(comment_data)
    if comment:
        response = {
            "message": "OK",
            "data": comment
        }
        return jsonify(response), 201
    else:
        response = {
            "error": "Failed to create comment."
        }
        return jsonify(response), 500
    

# Route pour récupérer tous les commentaires pour une vidéo spécifique avec pagination
@comment_bp.route('/video/<int:video_id>/comments', methods=['GET'])
def get_comments_route(video_id):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 10))

    comments, total_comments = get_comments_for_video(video_id, page, per_page)
    response = {
        "message": "OK",
        "data": comments,
        'pager':{
            "current": page,
            "total": (total_comments + per_page - 1) // per_page
        }
    }

    return jsonify(response), 200


# Route pour supprimer un commentaire
@comment_bp.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment_route(comment_id):
    if delete_comment(comment_id):
        response = {
            "message": "OK"
        }
        return jsonify(response), 200
    else:
        response = {
            "error": "Failed to delete comment."
        }
        return jsonify(response), 500
