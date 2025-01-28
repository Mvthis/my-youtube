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


# Connexion à la base de données
db_connection = Connection(host=db_host, port=db_port, database=db_name,
                           user=db_user, password=db_password)
db_connection.connect()

# Fonctions

# Création du secret key
jwt_secret_key = os.getenv("JWT_SECRET_KEY")

# ...

# Fonction pour s'authentifier
def authenticate_user(username, password):
    cursor = db_connection.get_connection().cursor()
    cursor.execute("SELECT id, username, password FROM user WHERE username = %s;", (username,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data:
        hashed_password_from_db = user_data[2].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db):
            user_dict = {
                'id': user_data[0],
                'username': user_data[1]
            }

            token = jwt.encode(user_dict, jwt_secret_key, algorithm='HS256')
            return token

    return None

# Fonction pour stocker le token dans la base de données
def store_token_in_database(token, user_id):
    pass

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