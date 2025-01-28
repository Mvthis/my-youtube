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


# Récupération de tous les utilisateurs avec pagination 
def get_users(page, items_per_page):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("SELECT * FROM user LIMIT %s OFFSET %s;", (items_per_page, (page - 1) * items_per_page))
    users = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM user;")
    total_users = cursor.fetchone()[0]
    cursor.close()
    return users, total_users


# Récupération d'un utilisateur par son ID
def get_user(user_id):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("SELECT * FROM user WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user
    
# Création d'un utilisateur
def create_user(user):
    hashed_password = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
    cursor = db_connection.get_connection().cursor()
    cursor.execute(
        "INSERT INTO user (username, email, pseudo, password) VALUES (%s, %s, %s, %s);",
        (user['username'], user['email'], user['pseudo'], hashed_password)
    )
    db_connection.get_connection().commit()
    cursor.execute("SELECT * FROM user WHERE username = %s;", (user['username'],))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data



# Suppression d'un utilisateur
def delete_user(user_id):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("DELETE FROM video WHERE user_id = %s;", (user_id,))
    cursor.execute("DELETE FROM comment WHERE user_id = %s;", (user_id,))
    cursor.execute("DELETE FROM token WHERE user_id = %s;", (user_id,))
    cursor.execute("DELETE FROM user WHERE id = %s;", (user_id,))
    cursor.close()
    db_connection.get_connection().commit()
    return True


# Modification d'un utilisateur
def update_user(user_id, user):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("UPDATE user SET username = %s, email = %s, pseudo = %s, password = %s WHERE id = %s;",
                   (user['username'], user['email'], user['pseudo'], user['password'], user_id))
    db_connection.get_connection().commit()
    cursor.execute("SELECT * FROM user WHERE id = %s;", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    return user_data
