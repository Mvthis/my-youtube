from flask import Flask, request, jsonify
import requests
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)


# Fonction pour envoyer un e-mail
def send_email(adresse_email, sujet, contenu):
    msg = Message(sujet, sender='mathismadode@gmail.com', recipients=[adresse_email])
    msg.body = contenu

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {str(e)}")
        return False