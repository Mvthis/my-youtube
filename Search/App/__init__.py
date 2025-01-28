from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from algoliasearch.search_client import SearchClient
from Services import *
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:5432"]}})


# Configuration Algolia
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")


client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)


index = client.init_index("myYoutube")

@app.route('/')
def home():
    return "Search"

@app.route('/update', methods=['GET'])
def update():
    # Fetch all videos from your local database
    videos = get_videos().json()["data"]

    # Fetch all objects from Algolia index
    existing_objects = index.browse_objects()

    # Create a set of existing objectIDs in Algolia
    existing_object_ids = set(obj["objectID"] for obj in existing_objects)

    # Create a set of objectIDs from your local database
    local_object_ids = set(video["id"] for video in videos)

    # Calculate the objectIDs to delete from Algolia (those not in the local database)
    object_ids_to_delete = existing_object_ids - local_object_ids

    # Delete objects from Algolia that are not in the local database
    for object_id in object_ids_to_delete:
        index.delete_object(object_id)

    # Format and save the remaining videos to Algolia
    formatted_data = [
        {"objectID": video["id"], "id": video["id"], "name": video["name"], "description": video["description"], "duration": video["duration"], "image": video["image"], "source": video["source"], "user_id": video["user_id"], "username": video["username"]}
        for video in videos
    ]
    index.save_objects(formatted_data).wait()

    response = {
        "message": "OK",
        "data": videos
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5460, debug=True)
