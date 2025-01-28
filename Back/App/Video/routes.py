import connexion
import uuid
from flask import Blueprint, request, jsonify, current_app as app
from flask import url_for
import os
import requests
import time 

from .service import *

videos_bp = Blueprint('videos', __name__)


# Route pour récupérer toutes les videos avec pagination
@videos_bp.route('/videos', methods=['GET'])
def get_videos_route():
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))
    videos, total_videos = get_videos(page, items_per_page)

    response = {
        "message": "OK",
        "data": videos,
        'pager':{
            "current": page,
            "total": (total_videos + items_per_page - 1) // items_per_page
        }
    }

    return jsonify(response), 200

# Route pour récupérer toutes les videos sans pagination
@videos_bp.route('/videos/all', methods=['GET'])
def get_all_videos_route():
    videos = get_all_videos()
    response = {
        "message": "OK",
        "data": videos
    }
    return jsonify(response), 200


# Route pour récupérer toutes les videos d'un utilisateur
@videos_bp.route('/user/<int:user_id>/videos', methods=['GET'])
def get_videos_by_user_route(user_id):
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('items_per_page', 10))

    videos, total_videos = get_videos_by_user(user_id, page, items_per_page)

    response = {
        "message": "OK",
        "data": videos,
        'pager':{
            "current": page,
            "total": (total_videos + items_per_page - 1) // items_per_page
        }
    }

    return jsonify(response), 200


# Route pour créer une video
@videos_bp.route('/user/<int:user_id>/video', methods=['POST'])
def create_user_video_route(user_id):
    token = verify_token(connexion.request.headers.get('Authorization'))
    if not token:
        return  jsonify({"message": "Unauthorized"}), 401
    uploaded_video = request.files.get('source')
    uploaded_image = request.files.get('image')
    
    if not uploaded_video:
        return jsonify({"error": "No video uploaded."}), 400
    
    video_name = request.form.get('name')
    video_description = request.form.get('description')
    username = request.form.get('username')

    unique_filename = str(uuid.uuid4())
    video_extension = os.path.splitext(uploaded_video.filename)[1]
    video_filename = f"{unique_filename}{video_extension}"
    
    video_folder_path = os.path.join(app.root_path, 'public', 'Video')
    os.makedirs(video_folder_path, exist_ok=True)
    video_file_path = os.path.join(video_folder_path, video_filename)
    uploaded_video.save(video_file_path)

    video_clip = VideoFileClip(video_file_path)
    video_duration = video_clip.duration
    video_clip.close()
    
    if uploaded_image:
        image_extension = os.path.splitext(uploaded_image.filename)[1]
        image_filename = f"{unique_filename}_image{image_extension}"
        
        image_folder_path = os.path.join(app.root_path, 'public', 'Image')
        os.makedirs(image_folder_path, exist_ok=True)
        image_file_path = os.path.join(image_folder_path, image_filename)
        uploaded_image.save(image_file_path)
    else:
        image_filename = None
    
    video = {
        'name': video_name,
        'description': video_description,
        'duration': video_duration,
        'user_id': user_id,
        'username': username,
        'source': url_for('uploaded_video', filename=video_filename),  
        'image': url_for('uploaded_image', filename=image_filename) if image_filename else None,
        'view': 0,
        'enabled': 1
    }
    
    video_data = create_video(video)
    if video_data:
        videoPath = "/Users/mvthis/ETNA/MyYoutube/group-1010709/Back/App/public/Video/"+video_filename
        
        # Appel de l'encodage
        requests.post('http://localhost:5450/encode', data={'video_path': videoPath, "video_id": video_data[0]})

        # Appel de l'indexation
        requests.get('http://localhost:5460/update')

        # Attente de 15 secondes pour laisser le temps à l'indexation de se faire
        time.sleep(15)

        # Appel de la notification
        requests.post('http://localhost:5451/video/upload/' + str(user_id))

        response = {
            "message": "Video created successfully.",
            "data": video_data
        }
        return jsonify(response), 201
    else:
        response = {
            "error": "Failed to create video."
        }
        return jsonify(response), 500


# Récupérer une video par son ID
@videos_bp.route('/video/<int:video_id>', methods=['GET'])
def get_video_route(video_id):
    video = get_video(video_id)
    if video:
        response = {
            "message": "OK",
            "data": video
        }
        return jsonify(response), 200
    else:
        response = {
            "error": "Video not found."
        }
        return jsonify(response), 404
    

# Route pour modifier une video
@videos_bp.route('/video/<int:video_id>', methods=['PUT'])
def update_video_route(video_id):
    token = verify_token(connexion.request.headers.get('Authorization'))
    if not token:
        return 401
    video = connexion.request.get_json()
    video = update_video(video_id, video)
    if video:
        response = {
            "message": "OK",
            "data": video
        }
        return jsonify(response), 200
    else:
        return 500
    

# Route pour supprimer une video
@videos_bp.route('/video/<int:video_id>', methods=['DELETE'])
def delete_video_route(video_id):
    token = verify_token(connexion.request.headers.get('Authorization'))
    if not token:
        return jsonify({"message": "Unauthorized"}), 401

    video = get_video(video_id)
    if not video:
        return jsonify({"message": "Video not found"}), 404

    delete_video_files(video)
    delete_video_from_db(video_id)

    requests.get('http://localhost:5460/update')

    response = {
        "message": "Vidéo supprimée avec succès.",
        "data": {
            "video": video
        }
    }
    return jsonify(response), 200

    

# Route pour encoder une video
@videos_bp.route('/video/<int:video_id>', methods=['POST'])
def save_encoding(video_id):
    # token = verify_token(connexion.request.headers.get('Authorization'))
    # if not token:
    #     return 401
    video_path = request.form.get('video_path')
    resolution = request.form.get('resolution')
    save = save_encoding_service(video_id, video_path, resolution)
    if save:
        response = {
            "message": "OK",
            "data": save
        }
        return jsonify(response), 200
    else:
        return  jsonify({"error": "Internal Server Error"}), 500 
    
    
# Route pour récupérer les videos encodées
@videos_bp.route('/video/<int:video_id>/encoded', methods=['GET'])
def get_encoded_video(video_id):
    encoded_video = get_video_formats(video_id)
    response = {
        "message": "OK",
        "data": encoded_video
    }
    return jsonify(response), 200