from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to the Flask API"

@app.route('/api/albums', methods=['GET'])
def get_albums():
    albums = [
        {"image": "/public/ash.png", "name": "Album 1", "similarity": 0.9},
        {"image": "/public/eiji.jpg", "name": "Album 2", "similarity": 0.85},
        # Add more album data
    ]
    return jsonify(albums)

@app.route('/api/music', methods=['GET'])
def get_music():
    music = [
        {"image": "/public/I_Want_It_That_Way.mid", "name": "Music 1", "similarity": 0.9},
        {"image": "/public/town-10169.mp3", "name": "Music 2", "similarity": 0.85},
        # Add more music data
    ]
    return jsonify(music)

if __name__ == '__main__':
    app.run(debug=True)