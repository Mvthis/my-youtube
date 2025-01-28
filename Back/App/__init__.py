from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from Auth.routes import auth_bp
from User.routes import users_bp
from Video.routes import videos_bp
from Comment.routes import comment_bp


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5451"]}})

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'public')
app.config['UPLOAD_FOLDER_IMAGE'] = os.path.join(app.config['UPLOAD_FOLDER'], 'Image')
app.config['UPLOAD_FOLDER_VIDEO'] = os.path.join(app.config['UPLOAD_FOLDER'], 'Video')

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='')
app.register_blueprint(videos_bp, url_prefix='')
app.register_blueprint(comment_bp, url_prefix='')


@app.route('/')
def home():
    return "MyAPI"

# Route to serve uploaded images
@app.route('/public/Image/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_IMAGE'], filename)

# Route to serve uploaded videos
@app.route('/public/Video/<filename>')
def uploaded_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_VIDEO'], filename)

if __name__ == '__main__':
    app.run(port=5432, debug=True)