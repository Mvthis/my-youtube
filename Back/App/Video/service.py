from flask import jsonify, current_app as app
from mysql.connector import Error
import bcrypt
from Connexion import Connection
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv
import jwt


# Chargement des variables d'environnement
load_dotenv()

# Variables d'environnement
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")


# Connexion à la base de données
db_connection = Connection(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
db_connection.connect()

# Fonctions

# Vérification de la validité du token
def verify_token(authorization_header):
    if authorization_header.startswith("Bearer "):
        token = authorization_header.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
            user_id = decoded_token.get('id')
            if user_id is not None:
                return True
        except jwt.ExpiredSignatureError:
            pass
        except jwt.DecodeError:
            pass
    return False


# Création d'une video 
def create_video(video):
    conn = db_connection.get_connection()

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO video (name, description, duration, user_id, username, source, image, view, enabled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
        (video['name'], video['description'], video['duration'], video['user_id'], video['username'], video['source'], video['image'], 0, 1)
    )
    conn.commit()
    cursor.execute("SELECT * FROM video WHERE name = %s;", (video['name'],))
    video_data = cursor.fetchall()
    cursor.close()
    return video_data



# Récupérer toutes les videos avec pagination
def get_videos(page, items_per_page):
    cursor = db_connection.get_connection().cursor()
    offset = (page - 1) * items_per_page
    query = f"SELECT * FROM video LIMIT {items_per_page} OFFSET {offset};"
    cursor.execute(query)
    videos = cursor.fetchall()

    video_data_list = [] 
    for video in videos:
        video_data = {
            'id': video[0],
            'name': video[1],
            'description': video[2],
            'duration': video[3],
            'user_id': video[4],
            'username': video[10],
            'source': video[5],
            'image': video[6],
        }
        video_data_list.append(video_data)
    
    cursor.execute("SELECT COUNT(*) FROM video;")
    total_videos = cursor.fetchone()[0]
    cursor.close()
    return video_data_list, total_videos

# Récupérer toutes les videos sans pagination
def get_all_videos():
    cursor = db_connection.get_connection().cursor()
    query = f"SELECT * FROM video;"
    cursor.execute(query)
    videos = cursor.fetchall()

    video_data_list = [] 
    for video in videos:
        video_data = {
            'id': video[0],
            'name': video[1],
            'description': video[2],
            'duration': video[3],
            'user_id': video[4],
            'username': video[10],
            'source': video[5],
            'image': video[6],
        }
        video_data_list.append(video_data)
    
    cursor.close()
    return video_data_list


# Récupérer toutes les videos d'un utilisateur avec pagination
def get_videos_by_user(user_id, page, items_per_page):
    cursor = db_connection.get_connection().cursor()
    offset = (page - 1) * items_per_page
    query = f"SELECT * FROM video WHERE user_id = {user_id} LIMIT {items_per_page} OFFSET {offset};"
    cursor.execute(query)
    videos = cursor.fetchall()

    video_data_list = []  
    for video in videos:
        video_data = {
            'id': video[0],
            'name': video[1],
            'description': video[2],
            'duration': video[3],
            'user_id': video[4],
            'username': video[10],
            'source': video[5],
            'image': video[6],
        }
        video_data_list.append(video_data)


    cursor.execute(f"SELECT COUNT(*) FROM video WHERE user_id = {user_id};")
    total_videos = cursor.fetchone()[0]
    cursor.close()
    return video_data_list, total_videos


# Récupérer une video par son ID
def get_video(video_id):
    try:
        cursor = db_connection.get_connection().cursor()
        cursor.execute("SELECT * FROM video WHERE id = %s;", (video_id,))
        video = cursor.fetchone()
        if video:
            video_data = {
                'id': video[0],
                'name': video[1],
                'description': video[2],
                'duration': video[3],
                'user_id': video[4],
                'username': video[10],
                'source': video[5],
                'image': video[6],
            }
            return video_data
        return None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
    
   



# Modification d'une video
def update_video(video_id, video):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("UPDATE video SET name = %s, duration = %s, user_id = %s, source = %s, view = %s, enabled = %s WHERE id = %s;",
                (video['name'], video['duration'], video['user_id'], video['source'], 0, 1, video_id))
    db_connection.get_connection().commit()
    cursor.execute("SELECT * FROM video WHERE id = %s;", (video_id,))
    video_data = cursor.fetchone()
    cursor.close()
    return video_data


# Supprimer la video
def delete_video_from_db(video_id):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("DELETE FROM comment WHERE video_id = %s;", (video_id,))
    cursor.execute("DELETE FROM video_format WHERE video_id = %s;", (video_id,))
    cursor.execute("DELETE FROM video WHERE id = %s;", (video_id,))
    cursor.close()
    db_connection.get_connection().commit()
    return "Vidéo supprimée", 204


# Supprimer la video et les fichiers associés
def delete_video_files(video):
    if video['source']:
        video_filename = os.path.basename(video["source"])
        video_file_path = os.path.join(app.root_path, 'public', 'Video', video_filename)
        if os.path.exists(video_file_path):
            os.remove(video_file_path)

    if video['image']:
        image_filename = os.path.basename(video['image'])
        image_file_path = os.path.join(app.root_path, 'public', 'Image', image_filename)
        if os.path.exists(image_file_path):
            os.remove(image_file_path)


# Encodage de la video
def save_encoding_service(video_id, video_path, resolution):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("INSERT INTO video_format (video_id, code, uri) VALUES (%s, %s, %s);", (video_id, resolution, video_path))
    db_connection.get_connection().commit()
    cursor.close()
    return "Vidéo encodée", 200

# Récupérer les formats d'une video
def get_video_formats(video_id):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("SELECT * FROM video_format WHERE video_id = %s;", (video_id,))
    video_formats = cursor.fetchall()

    video_formats_data_list = [] 
    for video_format in video_formats:
        split_uri = video_format[2].split('/')
        uri = f"http://localhost:5432/public/Video/{split_uri[len(split_uri) - 1]}"
        video_format_data = {
            'id': video_format[0],
            'video_id': video_format[3],
            'code': video_format[1],
            'uri': uri,
        }
        video_formats_data_list.append(video_format_data)
    cursor.close()
    return video_formats_data_list
    