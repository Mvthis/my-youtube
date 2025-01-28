# My YouTube

My YouTube est une application de diffusion vidéo basée sur une architecture **microservices**. Le projet comprend un frontend Vue.js et quatre microservices assurant différentes fonctionnalités pour garantir scalabilité et modularité.

## 🛠️ Technologies

- **Frontend** : Vue.js (Nuxt.js)
- **Backend** : Python (Flask)
- **Encodage vidéo** : Python (Flask) avec FFmpeg
- **Mailer** : Python (Flask)
- **Moteur de recherche** : Algolia
- **Base de données** : MySQL
- **Conteneurisation** : Docker (docker-compose)

## 📁 Structure

1. **Frontend** : Interface utilisateur permettant :
   - Gestion des utilisateurs (inscription, connexion, modification).
   - Upload et gestion des vidéos.
   - Recherche et consultation des vidéos.
2. **Backend API** : Gère les utilisateurs et les vidéos via des endpoints RESTful.
3. **Encodage vidéo** : Automatisation de l’encodage en différentes résolutions via FFmpeg.
4. **Mailer** : Envoi d’emails transactionnels (ex. : confirmation d’encodage).
5. **Moteur de recherche** : Recherche syntaxique rapide avec Algolia.

## 🚀 Déploiement

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/Mvthis/my-youtube.git
   cd my-youtube
   ```
