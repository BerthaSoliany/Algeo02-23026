import numpy as np
from PIL import Image
import os
import time
import scipy.linalg
from scipy.spatial.distance import pdist

# yang sifatnya interchangeable: target_size (di dalam load_and_process_image), k (di dalam set_pca), top_n
def nearest_neighbor(img_array, target_size):
    
    original_height, original_width = img_array.shape
    target_height, target_width = target_size

    # Skala transformasi
    scale_y = original_height / target_height
    scale_x = original_width / target_width

    # Array kosong untuk menyimpan gambar hasil resize
    resized_array = np.zeros((target_height, target_width))

    # Iterasi piksel target
    for i in range(target_height):
        for j in range(target_width):
            
            # Koordinat di gambar asli
            src_y = int(i * scale_y)
            src_x = int(j * scale_x)

            # Ambil nilai dari piksel asli (nearest neighbor)
            resized_array[i, j] = img_array[src_y, src_x]

    return resized_array

def load_and_process_image(image_path, dataset, folder_path):

    # Memuat gambar
    if dataset:
        image_path = os.path.join(folder_path, image_path)
    img = Image.open(image_path)
    
    # Mengonversi ke array NumPy (format RGB)
    img_array = np.asarray(img)
    
    # Melakukan konversi manual ke grayscale
    if len(img_array.shape) == 3:  # Jika gambar berwarna (RGB)
        R, G, B = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
        grayscale_array = 0.2989 * R + 0.5870 * G + 0.1140 * B
    else:  # Jika gambar sudah grayscale
        grayscale_array = img_array
    
    # Mengubah ukuran array ke dimensi target secara manual
    target_size = (64, 64)
    resized_array = nearest_neighbor(grayscale_array, target_size)
    
    # Mengubah array 2D menjadi vektor 1D
    img_vector = resized_array.flatten()
    
    return img_vector

def standarized_dataset(processed_images):
    
    # Menggabungkan semua array hasil pemrosesan gambar
    dataset = np.array(processed_images)

    # Hitung rata-rata piksel untuk setiap posisi
    mean_pixel_values = np.mean(dataset, axis=0)

    # Lakukan data centering
    centered_dataset = dataset - mean_pixel_values

    return mean_pixel_values, centered_dataset

def set_pca(centered_dataset):

    centered_dataset_scaled = centered_dataset / np.sqrt(centered_dataset.shape[0])

    # Lakukan Singular Value Decomposition (SVD)
    U, S, Ut = scipy.linalg.svd(centered_dataset_scaled, full_matrices=False)

    explained_variance = (S ** 2) / np.sum(S ** 2)
    cumulative_variance = np.cumsum(explained_variance)

    # Pilih k komponen utama    
    k = np.argmax(cumulative_variance >= 0.9) + 1
    eigenvectors = Ut.T[:, :k]
    # print(f"shape eigenvectors: {eigenvectors.shape}")

    # Proyeksikan data ke komponen utama
    projected_dataset = np.dot(centered_dataset, eigenvectors)

    return eigenvectors, projected_dataset

def set_pca_without_cov(centered_dataset):

    N = centered_dataset.shape[0]
    centered_dataset = np.transpose(centered_dataset) / (N**0.5)

    # Lakukan Singular Value Decomposition (SVD)
    U, S, Ut = scipy.linalg.svd(centered_dataset, full_matrices=False)

    # Pilih k komponen utama
    k = 10
    eigenvectors = U[:, :k] * S[:k]  # Skalakan eigenvector dengan nilai singular

    # Normalisasi eigenvector
    eigenvectors = eigenvectors / np.linalg.norm(eigenvectors, axis=0)

    # Proyeksikan data ke komponen utama
    centered_dataset = np.transpose(centered_dataset)
    projected_dataset = np.dot(centered_dataset, eigenvectors)

    return eigenvectors, projected_dataset

def validate_query_file(query_path):
    
    # Ekstensi yang diizinkan
    allowed_extensions = {'.jpg', '.png', '.jpeg'}
    
    # Ambil ekstensi file
    _, ext = os.path.splitext(query_path)
    
    # Periksa apakah ekstensi file valid
    if ext.lower() not in allowed_extensions:
        raise ValueError(f"File {query_path} memiliki format yang tidak valid. "
                         f"Harap gunakan file dengan ekstensi .jpg, .png, atau .jpeg.")
    return query_path

def project_to_pca(query_vector, mean_pixel_values, eigenvectors):
    
    # Mengurangi rata-rata gambar dari dataset (mean normalization)
    normalized_query = query_vector - mean_pixel_values
    
    # Proyeksi gambar query ke ruang komponen utama
    projected_query = np.dot(normalized_query, eigenvectors)
    
    return projected_query

def compute_euclidean_distance(projected_query_vector, projected_dataset):
    
    distances = []
    max_distance = np.max(pdist(projected_dataset))
    
    for i, vector in enumerate(projected_dataset):
        
        # Menghitung jarak Euclidean   
        distance = np.linalg.norm(projected_query_vector - vector)  
        distances.append((i, distance))
    
    # Urutkan berdasarkan jarak terkecil
    distances.sort(key=lambda x: x[1])

    # Normalisasi jarak menjadi persentase
    normalized_distances = [
        (index, max(0, min(100, 100 * (1 - distance / max_distance)))) for index, distance in distances
    ]
    
    return normalized_distances

def get_image_paths(similarities, image_paths):

    final_lists = []

    for i, value in similarities:
        final_list = {"name": image_paths[i], "similarity": value}
        final_lists.append([final_list])

    return final_lists

if __name__ == "__main__":

    start = time.time()

    folder_path = "./test/images"

    image_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                relative_path = os.path.relpath(os.path.join(root, file), folder_path)
                image_paths.append(relative_path)

    # print(image_paths)

    processed_images = [load_and_process_image(image_path, dataset=True, folder_path=folder_path) for image_path in image_paths]

    mean_pixel_values, centered_dataset = standarized_dataset(processed_images)

    eigenvectors, projected_dataset = set_pca(centered_dataset)

    query_paths = ["./test/query.jpg", "./test/query.png", "./test/query.jpeg"]
    for query_path in query_paths:
        try:
            query_path = validate_query_file(query_path)
            print(f"Query file {query_path} diproses.")
            break
        except ValueError as e:
            print(e)

    query_vector = load_and_process_image(query_path, dataset=False, folder_path=None)

    projected_query_vector = project_to_pca(query_vector, mean_pixel_values, eigenvectors)

    similarities = compute_euclidean_distance(projected_query_vector, projected_dataset)

    final_lists = get_image_paths(similarities, image_paths)

    i = 0
    for final_list in final_lists:
        print(final_lists[i])
        i += 1

    end = time.time()
    print(end - start)