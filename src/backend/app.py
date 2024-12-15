import os
import zipfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil
import numpy as np
from mido import MidiFile
from functions.MIR import (
    load_midi_file_considering_main_channel,
    find_most_similar_midi,
    fix_invalid_bytes
)

app = Flask(__name__)
CORS(app)

# direktori
QUERY_UPLOAD_FOLDER = './query_files'
DATASET_UPLOAD_FOLDER = './uploaded_datasets'
EXTRACT_FOLDER = './extracted_datasets'

os.makedirs(QUERY_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

# bersihkan direktori setiap upload query atau dataset baru
def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# endpoint untuk mengunggah dataset
@app.route('/upload-dataset', methods=['GET', 'POST'])
def upload_dataset():
    if request.method == 'GET':
        return "Upload dataset endpoint is active!"

    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        print("No file selected")
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith('.zip'):
        print("Invalid file format")
        return jsonify({'error': 'Only ZIP files are allowed'}), 400
    
    clear_directory(DATASET_UPLOAD_FOLDER)
    clear_directory(EXTRACT_FOLDER)

    zip_path = os.path.join(DATASET_UPLOAD_FOLDER, file.filename)
    try:
        file.save(zip_path)
        print(f"File saved at {zip_path}")
    except Exception as e:
        print(f"Failed to save file: {e}")
        return jsonify({'error': 'Failed to save file'}), 500

    extract_path = os.path.join(EXTRACT_FOLDER, os.path.splitext(file.filename)[0])
    os.makedirs(extract_path, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"File extracted to {extract_path}")
    except zipfile.BadZipFile:
        print("Failed to extract ZIP file")
        return jsonify({'error': 'Invalid ZIP file'}), 400

    return jsonify({'message': 'Dataset uploaded and extracted successfully', 'extracted_folder': './extracted_datasets/cek_midi'})

# endpoint untuk mengunggah query
@app.route('/upload-query', methods=['POST'])
def upload_query():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not (file.filename.endswith('.mid') or file.filename.endswith('.midi') or file.filename.endswith('.jpg') or file.filename.endswith('.jpeg') or file.filename.endswith('.png')):
        return jsonify({'error': 'Invalid file format. Only MIDI or image files are allowed.'}), 400

    clear_directory(QUERY_UPLOAD_FOLDER)

    file_path = os.path.join(QUERY_UPLOAD_FOLDER, secure_filename(file.filename))
    try:
        file.save(file_path)
        print(f"Query file saved at {file_path}")
    except Exception as e:
        print(f"Failed to save query file: {e}")
        return jsonify({'error': 'Failed to save query file'}), 500

    return jsonify({'message': 'Query file uploaded successfully', 'file_path': file_path})

# endpoint untuk menghitung similarity
similarity_results = None
@app.route('/process-similarity', methods=['POST'])
def process_similarity():
    global similarity_results
    try:
        if not os.listdir(QUERY_UPLOAD_FOLDER):
            return jsonify({'success': False, 'error': 'No query file uploaded'})

        query_file = os.path.join(QUERY_UPLOAD_FOLDER, os.listdir(QUERY_UPLOAD_FOLDER)[0])

        processed_audios = []
        audio_names = []

        # Proses semua file MIDI dalam dataset
        for root, _, files in os.walk(EXTRACT_FOLDER):
            for file in files:
                if file.endswith('.mid') or file.endswith('.midi'):
                    audio_names.append(file)
                    file_path = os.path.join(root, file)
                    try:
                        fix_invalid_bytes(file_path, file_path)
                        db_notes = load_midi_file_considering_main_channel(file_path)
                        processed_audios.append(db_notes)
                    except Exception as e:
                        print(f"Failed to process file {file_path}: {e}")

        # Hitung similarity
        similarities = find_most_similar_midi(query_file, processed_audios)
        
        # Filter hasil similarity dengan threshold 80%
        threshold = 0.55
        filtered_results = [
            {
                "rank": i + 1,
                "file_name": audio_names[idx],
                "similarity": round(value * 100, 2),
                "audioSrc": f"http://127.0.0.1:5000/get-audio/{audio_names[idx]}"  # Tambahkan audioSrc URL
            }
            for i, (idx, value) in enumerate(similarities) if value >= threshold
        ]

        # Simpan hasil similarity global
        similarity_results = filtered_results

        return jsonify({
            'success': True,
            'results': filtered_results,
            'threshold': threshold
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-similarity-results', methods=['GET'])
def get_similarity_results():
    global similarity_results
    if similarity_results is None:
        return jsonify({'success': False, 'error': 'No similarity results available'})
    return jsonify({'success': True, 'results': similarity_results})

from flask import send_from_directory

# Endpoint untuk menyajikan file MIDI dari extracted_datasets
@app.route('/get-audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    try:
        return send_from_directory(EXTRACT_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)