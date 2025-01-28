import requests
from flask import current_app as app

def get_videos():
    videos = requests.get('http://localhost:5432/videos/all')
    return videos