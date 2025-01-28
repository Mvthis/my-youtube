from flask import jsonify
import bcrypt
from Connexion import Connection
import os
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
db_connection = Connection(host=db_host, port=db_port, database=db_name,
                           user=db_user, password=db_password)
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


# Fonction pour récupérer tous les commentaires pour une vidéo spécifique
def get_comments():
    cursor = db_connection.get_connection().cursor()
    cursor.execute("SELECT * FROM comment;")
    comments = cursor.fetchall()
    cursor.close()
    return jsonify(comments)


# Fonction pour récupérer tous les commentaires pour une vidéo spécifique avec pagination
def get_comments_for_video(video_id, page, per_page):
    cursor = db_connection.get_connection().cursor()
    
    offset = (page - 1) * per_page
    
    cursor.execute("SELECT * FROM comment WHERE video_id = %s LIMIT %s OFFSET %s;", (video_id, per_page, offset))
    comments = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM comment WHERE video_id = %s;", (video_id,))
    total_comments = cursor.fetchone()[0]
    
    cursor.close()
    
    # Format the comments with the desired keys
    formatted_comments = [{'id': comment[0], 'body': comment[2], 'username': comment[1], 'video_id': comment[4]} for comment in comments]
    
    return formatted_comments, total_comments


# Enregistrer un commentaire pour une vidéo spécifique
def create_comment(comment_data):
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "INSERT INTO comment (body, username, user_id, video_id) VALUES (%s, %s, %s, %s);",
        (comment_data['body'], comment_data['username'], comment_data['user_id'], comment_data['video_id'])
    )
    db_connection.get_connection().commit()
    cursor.execute("SELECT * FROM comment WHERE id = LAST_INSERT_ID();")
    comment = cursor.fetchone()
    cursor.close()
    return comment


# Supprimer un commentaire
def delete_comment(comment_id):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("DELETE FROM comment WHERE id = %s;", (comment_id,))
    db_connection.get_connection().commit()
    cursor.close()
    return True
