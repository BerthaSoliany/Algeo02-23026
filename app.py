from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from src.functions.mapper import generate_mapper_from_dataset_recursive

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to the Flask API"

@app.route('/api/generate_mapper_recursive', methods=['POST'])
def generate_mapper_recursive_api():
    image_directory = './test/images'
    audio_directory = './test/audios'
    output_mapper_file = './test/mapper.json'

    mapper = generate_mapper_from_dataset_recursive(image_directory, audio_directory, output_mapper_file)
    return jsonify({
        "message": "Mapper generated successfully",
        "mapper": mapper
    })

@app.route('/api/get_mapper', methods=['GET'])
def get_mapper():
    mapper_file = './test/mapper.json'  # Sesuaikan path
    try:
        with open(mapper_file, 'r') as file:
            mapper_data = json.load(file)
        return jsonify(mapper_data)
    except FileNotFoundError:
        return jsonify({"error": "Mapper file not found"}), 404


@app.route('/api/albums', methods=['GET'])
def get_albums():
    mapper_file = './test/mapper.json' 
    output_file = './test/output_image.json'
    try: 
        with open(mapper_file, 'r') as file:
            mapper_data = json.load(file)
        albums = [
            {"name": "guts.png", "similarity": 35.17},
            {"name": "I_Want_It_That_Way.jpg", "similarity": 57.91, "image": None},

        ]
        
        # print("Albums awal:", albums)

        for album in albums:
            matched = next((item for item in mapper_data if album['name'] in item['image']), None)
            # print(f"Matching album {album['name']} -> {matched}")
            if matched:
                album["image"] = f"{matched['image']}"
            else:
                album["image"] = None
        with open(output_file, 'w') as output:
            json.dump(albums, output, indent=4)
        # print("Hasil albums sebelum disimpan:", albums)
        return jsonify(albums)
    except FileNotFoundError:
        return jsonify({"error": "Mapper file not found"}), 404

@app.route('/api/music', methods=['GET'])
def get_music():
    mapper_file = './test/mapper.json'
    output_file = './test/output_music.json'
    try:
        with open(mapper_file, 'r') as file:
            mapper_data = json.load(file)
        music = [
            {"name": "Theme-From-'Beauty-And-The-Beast'-(Walt-Disney).mid", "similarity": 100},
            {"name": "I_Want_It_That_Way.mid", "similarity": 57.91, "image": None, "audioSrc": None},
        ]
        for track in music:
            matched = next((item for item in mapper_data if track['name'] in item['audioSrc']), None)
            if matched:
                track["image"] = f"{matched['image']}"
                track["audioSrc"] = f"{matched['audioSrc']}"
            else:
                track["image"] = None
                track["audioSrc"] = None
        # print("Hasil albums sebelum disimpan:", music)
        with open(output_file, 'w') as output:
            json.dump(music, output, indent=4)
        return jsonify(music)
    except FileNotFoundError:
        return jsonify({"error": "Mapper file not found"}), 404

def remove_extension(filename):
    return filename.rsplit('.', 1)[0]

@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    selected_album = request.args.get('album')

    try:
        with open('./test/mapper.json', 'r') as file:
            mapper_data = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "Mapper file not found"}), 404
    
    if not selected_album:
        return jsonify({"error": "No album selected"}), 404
    
    playlist =[]

    for item in mapper_data:
        album_name = remove_extension(selected_album)
        if album_name in item['image']:
            playlist.append({
                "title" : album_name,
                "albumSrc" : item['image'],
                "audioSrc" : item['audioSrc']
            })
    if not playlist:
        return jsonify({"message": "No matching songs found for the selected album"}), 404
    
    return jsonify(playlist)

@app.route('/public/<path:filename>')
def serve_public(filename):
    return send_from_directory(os.path.join(app.root_path, 'public'), filename)


# # Nama file yang ingin dicari
# file_name = "I_Want_It_That_Way.jpg"

# # Direktori dasar yang ingin dicari (misalnya di direktori 'test/images')
# search_directory = "test/images"

# # Fungsi untuk mencari file dalam folder dan subfolder
# def find_file_by_name(search_directory, file_name):
#     for root, dirs, files in os.walk(search_directory):
#         if file_name in files:
#             # Jika ditemukan, kembalikan path relatif
#             return os.path.relpath(os.path.join(root, file_name), start=search_directory)
#     return None  # Jika file tidak ditemukan

# # Mencari file
# relative_path = find_file_by_name(search_directory, file_name)

# if relative_path:
#     print("File ditemukan pada:", relative_path)
# else:
#     print("File tidak ditemukan.")


if __name__ == '__main__':
    app.run(debug=True)