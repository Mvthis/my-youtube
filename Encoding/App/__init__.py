from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from Services import *

app = Flask(__name__)
cors = CORS(app, resources={
            r"/*": {"origins": "http://localhost:3000"}, r"/*": {"origins": "http://localhost:5432"}})


@app.route('/')
def home():
    return "Encoder"

# Route d'encodage

@app.route('/encode', methods=['POST'])
def encode():
    video_path = request.form['video_path']
    video_id = request.form['video_id']
    is_encoded = encoding(video_path, video_id)
    if is_encoded:
        return jsonify({'success': True})
    else:
        return jsonify({'error': False})


if __name__ == '__main__':
    app.run(port=5450, debug=True)
