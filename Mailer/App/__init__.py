from flask import Flask, jsonify
from flask_cors import CORS
import requests
from Services import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5432"}})
app.config['MAIL_SERVER'] = 'localhost'  # Serveur SMTP de Postfix
app.config['MAIL_PORT'] = 25  # Port SMTP de Postfix
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'votre_nom_utilisateur'
app.config['MAIL_PASSWORD'] = 'votre_mot_de_passe'


# Route pour notifier l'utilisateur lors d'une modification de son compte
@app.route('/user/update/<int:user_id>', methods=['POST'])
def user_update(user_id):

    response = requests.get('http://127.0.0.1:5432/user/' + str(user_id))
    
    if response.status_code == 200:
        user = response.json()['data']
        email = user[2]
        print(email)

        sujet = 'Modification réussie'
        contenu = 'Vos informations ont été mises à jour avec succès.'
        
        if send_email(email, sujet, contenu):
            return jsonify({'message': 'Modification réussie et e-mail envoyé'}), 200
        else:
            return jsonify({'message': 'Modification réussie, mais erreur lors de l\'envoi de l\'e-mail'}), 500
    else:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404
    

# Route pour notifier l'utilisateur lors de la fin de l'upload d'une vidéo
@app.route('/video/upload/<int:user_id>', methods=['POST'])
def video_update(user_id):

    response = requests.get('http://127.0.0.1:5432/user/' + str(user_id))

    if response.status_code == 200:
        user = response.json()['data']
        email = user[2]
        print(email)

        sujet = 'Modification réussie'
        contenu = 'Votre vidéo a été mise en ligne avec succès.'
        
        if send_email(email, sujet, contenu):
            return jsonify({'message': 'Modification réussie et e-mail envoyé'}), 200
        else:
            return jsonify({'message': 'Modification réussie, mais erreur lors de l\'envoi de l\'e-mail'}), 500
    else:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404


if __name__ == '__main__':
    app.run(port=5451, debug=True)
