import os
import json
from concurrent.futures import ProcessPoolExecutor
import zipfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import shutil
import numpy as np
from mido import MidiFile
from flask import send_from_directory
from functions.MIR import (
    process_midi_file,
    find_most_similar_midi
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
from functions.mapper import generate_mapper_from_dataset_recursive

app = Flask(__name__)
CORS(app)

# direktori
QUERY_UPLOAD_FOLDER = './query_files'
DATASET_UPLOAD_FOLDER = './uploaded_datasets'
EXTRACT_FOLDER = './extracted_datasets'
DATASET_UPLOAD_IMAGE_FOLDER = './uploaded_datasets_image'
EXTRACT_IMAGE_FOLDER = './extracted_datasets_image'

# Buat direktori yang dibutuhkan jika belum ada
os.makedirs('./test', exist_ok=True)  # Untuk menyimpan mapper.json
os.makedirs(QUERY_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
os.makedirs(DATASET_UPLOAD_IMAGE_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_IMAGE_FOLDER, exist_ok=True)

# bersihkan direktori setiap upload query atau dataset baru
def clear_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)  # Pastikan direktori ada
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
@app.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    clear_directory(DATASET_UPLOAD_FOLDER)
    clear_directory(EXTRACT_FOLDER)
    clear_directory('./test')  # Pastikan direktori mapper dibuat

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.zip'):
        return jsonify({'error': 'Only ZIP files are allowed'}), 400

    zip_path = os.path.join(DATASET_UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(zip_path)

    extract_path = os.path.join(EXTRACT_FOLDER, os.path.splitext(file.filename)[0])
    os.makedirs(extract_path, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        return jsonify({'error': 'Invalid ZIP file'}), 400

    image_directory = './extracted_datasets_image'
    mapper_file = './test/mapper.json'

    if os.path.exists(image_directory) and os.listdir(image_directory):
        generate_mapper_from_dataset_recursive(image_directory, EXTRACT_FOLDER, mapper_file)
        return jsonify({
            'message': 'Dataset uploaded and mapper generated successfully',
            'extracted_folder': extract_path,
            'mapper_file': mapper_file
        })
    else:
        return jsonify({
            'message': 'Dataset uploaded but no images found. Mapper not generated.',
            'extracted_folder': extract_path
        })

# endpoint untuk mengunggah dataset gambar
@app.route('/upload-dataset-image', methods=['POST'])
def upload_dataset_image():
    clear_directory(DATASET_UPLOAD_IMAGE_FOLDER)
    clear_directory(EXTRACT_IMAGE_FOLDER)
    clear_directory('./test')  # Pastikan direktori mapper dibuat

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.zip'):
        return jsonify({'error': 'Only ZIP files are allowed'}), 400

    zip_path = os.path.join(DATASET_UPLOAD_IMAGE_FOLDER, secure_filename(file.filename))
    file.save(zip_path)

    extract_path = os.path.join(EXTRACT_IMAGE_FOLDER, os.path.splitext(file.filename)[0])
    os.makedirs(extract_path, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        return jsonify({'error': 'Invalid ZIP file'}), 400

    audio_directory = './extracted_datasets'
    mapper_file = './test/mapper.json'

    if os.path.exists(audio_directory) and os.listdir(audio_directory):
        generate_mapper_from_dataset_recursive(EXTRACT_IMAGE_FOLDER, audio_directory, mapper_file)
        return jsonify({
            'message': 'Image dataset uploaded and mapper generated successfully',
            'extracted_folder': extract_path,
            'mapper_file': mapper_file
        })
    else:
        return jsonify({
            'message': 'Image dataset uploaded but no audio dataset found. Mapper not generated.',
            'extracted_folder': extract_path
        })

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
        # Lokasi dataset
        image_directory = './extracted_datasets_image'
        audio_directory = './extracted_datasets'
        mapper_file = './test/mapper.json'

        # Pastikan direktori dan file yang diperlukan ada
        if not os.path.exists('./test'):
            os.makedirs('./test', exist_ok=True)

        # Baca query file
        if not os.listdir(QUERY_UPLOAD_FOLDER):
            return jsonify({'success': False, 'error': 'No query file uploaded'})

        query_file = os.path.join(QUERY_UPLOAD_FOLDER, os.listdir(QUERY_UPLOAD_FOLDER)[0])

        # Ambil semua file MIDI dalam dataset
        dataset_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(EXTRACT_FOLDER)
            for file in files if file.endswith('.mid') or file.endswith('.midi')
        ]

        if not dataset_files:
            return jsonify({'success': False, 'error': 'No MIDI files found in dataset'})

        # Parallel processing dataset
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(process_midi_file, dataset_files))

        # Filter file MIDI yang berhasil diproses
        processed_audios = [result for result in results if result is not None]

        # Ekstrak nama file untuk referensi
        audio_names = [os.path.basename(path) for path in dataset_files]

        # Temukan tingkat kemiripan menggunakan query file
        similarities = find_most_similar_midi(query_file, processed_audios)

        # Filter hasil berdasarkan threshold
        threshold = 0.55
        filtered_results = []
        for i, (idx, value) in enumerate(similarities):
            if value >= threshold:
                audio_name = audio_names[idx]

                # Jika mapper.json ada, tambahkan informasi gambar
                image_path = None
                if os.path.exists(mapper_file):
                    with open(mapper_file, 'r') as f:
                        mapper_data = json.load(f)
                        matched = next((item for item in mapper_data if audio_name in item['audioSrc']), None)
                        image_path = f"http://127.0.0.1:5000/extracted_datasets_image/{matched['image']}" if matched else None

                filtered_results.append({
                    "rank": i + 1,
                    "file_name": audio_name,
                    "similarity": round(value * 100, 2),
                    "audioSrc": f"http://127.0.0.1:5000/get-audio/{audio_name}",
                    "image": image_path
                })

        # Simpan hasil global
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
                "file_name": os.path.basename(result["name"]),  # Nama file untuk ditampilkan
                "image_path": result["name"],  # Path lengkap untuk URL gambar
                "similarity": round(result["similarity"], 2)  # Similarity dengan 2 desimal
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
        print(f"Serving file: {filename}")  # Debug log
        return send_from_directory(EXTRACT_IMAGE_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        print(f"File not found: {filename}")  # Debug log
        return jsonify({'error': 'File not found'}), 404

# Endpoint untuk mengunggah file mapper
@app.route('/upload-mapper', methods=['POST'])
def upload_mapper():
    MAPPER_FOLDER = './uploaded_mappers'
    os.makedirs(MAPPER_FOLDER, exist_ok=True)

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith('.json'):
        return jsonify({'error': 'Invalid file format. Only JSON files are allowed.'}), 400

    file_path = os.path.join(MAPPER_FOLDER, secure_filename(file.filename))

    try:
        file.save(file_path)
        print(f"Mapper file saved at {file_path}")
        return jsonify({'message': 'Mapper file uploaded successfully', 'file_path': file_path})
    except Exception as e:
        print(f"Failed to save mapper file: {e}")
        return jsonify({'error': 'Failed to save mapper file'}), 500

@app.route('/generate-mapper', methods=['POST'])
def generate_mapper():
    image_directory = './test/images'
    audio_directory = './test/audios'
    output_mapper_file = './test/mapper.json'

    try:
        mapper = generate_mapper_from_dataset_recursive(image_directory, audio_directory, output_mapper_file)
        return jsonify({
            "message": "Mapper generated successfully",
            "mapper": mapper
        })
    except Exception as e:
        return jsonify({'error': f"Failed to generate mapper: {str(e)}"}), 500

@app.route('/get-dataset-audio', methods=['GET'])
def get_dataset_audio():
    try:
        dataset_files = [
            {
                "name": file,
                "audioSrc": f"http://127.0.0.1:5000/get-audio/{file}",
            }
            for root, _, files in os.walk(EXTRACT_FOLDER)
            for file in files if file.endswith('.mid') or file.endswith('.midi')
        ]

        return jsonify({'success': True, 'data': dataset_files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-dataset-images', methods=['GET'])
def get_dataset_images():
    try:
        image_files = []
        for root, _, files in os.walk(EXTRACT_IMAGE_FOLDER):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, EXTRACT_IMAGE_FOLDER)
                    image_files.append({
                        "name": os.path.basename(file),
                        "image": f"http://127.0.0.1:5000/extracted_datasets_image/{relative_path.replace(os.sep, '/')}"
                    })
        
        print("Generated image URLs:", image_files)  # Debug log
        return jsonify({'success': True, 'data': image_files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)