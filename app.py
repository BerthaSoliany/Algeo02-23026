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
        # {"image": "./eiji.png", "name": "Album", "similarity": 0.9},
        # {"image": "./ash.png", "name": "Album 2", "similarity": 0.85},
        # Add more album data
        {"image": "./pinkthing.jpg", "name": "thankunext.jpg", "similarity": 68.17},
        {"image": "./purple.jpg", "name": "sour.png", "similarity": 77.75},
        {"image": "./happier.jpg", "name": "happierThanEver.png", "similarity": 77.50},
        {"image": "./1989.jpg", "name": "1989.png", "similarity": 76.29},
        {"image": "./sweetener.jpg", "name": "sweeteener.jpg", "similarity": 71.85},
        {"image": "./rainbow.jpg", "name": "lover.png", "similarity": 67.78},
        {"image": "./beigetaylor.jpg", "name": "Fearless.png", "similarity": 60.25},
        {"image": "./paradise.jpg", "name": "paradise.png", "similarity": 54.94},
        {"image": "./midnights.jpg", "name": "midnights.png", "similarity": 48.08},
        {"image": "./dangerous_woman.jpg", "name": "dangerous_woman.png", "similarity": 46.67},
        {"image": "./redtaylor.jpg", "name": "red.png", "similarity": 44.93},
        {"image": "./jungle.jpg", "name": "ctrl.png", "similarity": 43.35},
        {"image": "./secret.jpg", "name": "theSecretOfUs.png", "similarity": 39.26},
        {"image": "./guts.jpg", "name": "guts.png", "similarity": 35.17},
        {"image": "./ari.jpg", "name": "eternal_sunshine.png", "similarity": 28.91},
        {"image": "./car.jpg", "name": "futureNostalgia.png", "similarity": 26.04},

    ]
    return jsonify(albums)

@app.route('/api/music', methods=['GET'])
def get_music():
    music = [
        {"image": "./b.jpg", "name": "Theme-From-'Beauty-And-The-Beast'-(Walt-Disney).mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 100},
        {"image": "./b.jpg", "name": "Beauty_and_the_Beast.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 89.26},
        {"image": "./more.jpg", "name": "fixed_More_Than_That.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 63.02},
        {"image": "./more.jpg", "name": "More_Than_That.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 63.02},
        {"image": "./aslong.png", "name": "As_Long_as_You_Love_Me.2.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 59.7},
        {"image": "./aslong.png", "name": "fixed_As_Long_as_You_Love_Me.2.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 59.7},
        {"image": "./aslong.png", "name": "As_Long_as_You_Love_Me.5.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 59.56},
        {"image": "./aslong.png", "name": "fixed_As_Long_as_You_Love_Me.5.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 59.56},
        {"image": "./want.jpg", "name": "fixed_I_Want_It_That_Way.1.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 57.91},
        {"image": "./want.jpg", "name": "I_Want_It_That_Way.1.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 57.91},
        {"image": "./want.jpg", "name": "fixed_I_Want_It_That_Way.3.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 57.5},
        {"image": "./want.jpg", "name": "I_Want_It_That_Way.3.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 57.5},
        {"image": "./down.jpg", "name": "fixed_Get_Down.7.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 56.78},
        {"image": "./down.jpg", "name": "Get_Down.7.mid", "audioSrc": "./I_Want_It_That_Way.mid", "similarity": 56.78},



        # Add more music data
    ]
    return jsonify(music)

@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    music = [
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # {"title": "Music 1", "albumSrc": "./ash.png", "audioSrc": "./I_Want_It_That_Way.mid"},
        # Add more music data
        {"title": "Sweetener", "albumSrc": "./sweetener.jpg", "audioSrc": "./I_Want_It_That_Way.mid"},

    ]
    return jsonify(music)

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory(os.path.join(app.root_path, 'public'), filename)

if __name__ == '__main__':
    app.run(debug=True)