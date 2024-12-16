import os
import zipfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil
import numpy as np
from mido import MidiFile
from flask import send_from_directory
from functions.MIR import (
    load_midi_file_considering_main_channel,
    find_most_similar_midi,
    fix_invalid_bytes
)
from functions.AIR import (
    process_images_in_parallel,
    load_and_process_image,
    standarized_dataset,
    set_pca,
    validate_query_file,
    project_to_pca,
    compute_euclidean_distance,
    get_image_paths
)

app = Flask(__name__)
CORS(app)

# direktori
QUERY_UPLOAD_FOLDER = './query_files'
DATASET_UPLOAD_FOLDER = './uploaded_datasets'
EXTRACT_FOLDER = './extracted_datasets'
DATASET_UPLOAD_IMAGE_FOLDER = './uploaded_datasets_image'
EXTRACT_IMAGE_FOLDER = './extracted_datasets_image'

os.makedirs(QUERY_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
os.makedirs(DATASET_UPLOAD_IMAGE_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_IMAGE_FOLDER, exist_ok=True)

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

# endpoint untuk mengunggah dataset gambar
@app.route('/upload-dataset-image', methods=['POST'])
def upload_dataset_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '' or not file.filename.endswith('.zip'):
        return jsonify({'error': 'Only ZIP files are allowed'}), 400

    clear_directory(DATASET_UPLOAD_IMAGE_FOLDER)
    clear_directory(EXTRACT_IMAGE_FOLDER)

    zip_path = os.path.join(DATASET_UPLOAD_IMAGE_FOLDER, file.filename)
    file.save(zip_path)

    extract_path = os.path.join(EXTRACT_IMAGE_FOLDER, os.path.splitext(file.filename)[0])
    os.makedirs(extract_path, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        return jsonify({'error': 'Invalid ZIP file'}), 400

    return jsonify({'message': 'Dataset image uploaded and extracted successfully', 'extracted_folder': extract_path})

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

        similarities = find_most_similar_midi(query_file, processed_audios)
        
        threshold = 0.55
        filtered_results = [
            {
                "rank": i + 1,
                "file_name": audio_names[idx],
                "similarity": round(value * 100, 2),
                "audioSrc": f"http://127.0.0.1:5000/get-audio/{audio_names[idx]}"
            }
            for i, (idx, value) in enumerate(similarities) if value >= threshold
        ]

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

# endpoint untuk menghitung similarity gambar
image_similarity_results = None
@app.route('/process-image-similarity', methods=['POST'])
@app.route('/process-image-similarity', methods=['POST'])
def process_image_similarity():
    try:
        if not os.listdir(QUERY_UPLOAD_FOLDER):
            return jsonify({'success': False, 'error': 'No query file uploaded'})

        query_file = os.path.join(QUERY_UPLOAD_FOLDER, os.listdir(QUERY_UPLOAD_FOLDER)[0])
        
        try:
            query_file = validate_query_file(query_file)
        except ValueError as e:
            return jsonify({'success': False, 'error': str(e)})

        folder_path = EXTRACT_IMAGE_FOLDER
        image_paths = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                    image_paths.append(relative_path)

        if not image_paths:
            return jsonify({'success': False, 'error': 'No images found in dataset'})

        # Memproses gambar dataset menggunakan threading
        processed_images = process_images_in_parallel(image_paths, dataset=True, folder_path=folder_path)

        # Standarisasi dataset
        mean_pixel_values, centered_dataset = standarized_dataset(processed_images)

        # PCA pada dataset
        eigenvectors, projected_dataset = set_pca(centered_dataset)

        # Proses query image
        query_vector = load_and_process_image(query_file, dataset=False)
        projected_query_vector = project_to_pca(query_vector, mean_pixel_values, eigenvectors)

        # Hitung similarity
        similarities = compute_euclidean_distance(projected_query_vector, projected_dataset)

        # Ambil path gambar dengan similarity
        final_lists = get_image_paths(similarities, image_paths)

        # Filter hasil dengan threshold dan format similarity
        threshold = 55  # 55% similarity threshold
        filtered_results = [
            {
                "file_name": result["name"],
                "similarity": round(result["similarity"], 2)  # Round to 2 decimal places
            }
            for result_list in final_lists
            for result in result_list
            if result["similarity"] >= threshold
        ]

        return jsonify({
            'success': True,
            'results': filtered_results,
            'threshold': threshold
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-image-similarity-results', methods=['GET'])
def get_image_similarity_results():
    global image_similarity_results
    if image_similarity_results is None:
        return jsonify({'success': False, 'error': 'No similarity results available'})
    return jsonify({'success': True, 'results': image_similarity_results})

# endpoint untuk menyajikan file MIDI dari extracted_datasets
@app.route('/get-audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    try:
        return send_from_directory(EXTRACT_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

# endpoint untuk menyajikan file gambar dari extracted_datasets_image
@app.route('/extracted_datasets_image/<path:filename>', methods=['GET'])
def get_image(filename):
    try:
        return send_from_directory(EXTRACT_IMAGE_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)