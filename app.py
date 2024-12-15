from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to the Flask API"

@app.route('/api/albums', methods=['GET'])
def get_albums():
    albums = [
        {"image": "./eiji.png", "name": "Album", "similarity": 0.9},
        {"image": "./ash.png", "name": "Album 2", "similarity": 0.85},
        # Add more album data
    ]
    return jsonify(albums)

@app.route('/api/music', methods=['GET'])
def get_music():
    music = [
        {"image": "./letter.png", "name": "Music 1", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 0.9},
        {"image": "./max.jpg", "name": "Music 2", "audioSrc": "./town-10169.mp3", "similarity": 0.85},
        # Add more music data
    ]
    return jsonify(music)

@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    music = [
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # Add more music data
    ]
    return jsonify(music)

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory(os.path.join(app.root_path, 'public'), filename)

if __name__ == '__main__':
    app.run(debug=True)