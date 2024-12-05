import numpy as np
from PIL import Image
import os
import time

# yang sifatnya interchangeable: target_size (di dalam load_and_process_image), k, top_n
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

def load_and_process_image(image_path, dataset):

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
    target_size = (20, 20)
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

    # Hitung matriks kovarians
    C = np.cov(centered_dataset, rowvar=False)  # Covariance matrix (H*W x H*W)

    # Lakukan Singular Value Decomposition (SVD)
    U, S, Ut = np.linalg.svd(C)

    # Pilih k komponen utama (misal k=50)
    k = 50
    eigenvectors = U[:, :k]  # Ambil k eigenvector teratas (H*W x k)

    # Proyeksikan data ke komponen utama
    projected_dataset = np.dot(centered_dataset, eigenvectors)  # Z adalah data terproyeksi (N x k)

    return eigenvectors, projected_dataset

def project_to_pca(query_vector, mean_pixel_values, eigenvectors):
    
    # Mengurangi rata-rata gambar dari dataset (mean normalization)
    normalized_query = query_vector - mean_pixel_values
    
    # Proyeksi gambar query ke ruang komponen utama
    projected_query = np.dot(normalized_query, eigenvectors)
    
    return projected_query

def compute_euclidean_distance(projected_query_vector, projected_dataset):
    
    distances = []
    
    for i, vector in enumerate(projected_dataset):
        
        # Menghitung jarak Euclidean   
        distance = np.linalg.norm(projected_query_vector - vector)  
        distances.append((i, distance))
    
    # Urutkan berdasarkan jarak terkecil
    distances.sort(key=lambda x: x[1])
    
    return distances

if __name__ == "__main__":

    start = time.time()

    folder_path = "../test/images"
    image_paths = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    print("hasil image_paths:", image_paths)

    processed_images = [load_and_process_image(image_path, dataset=True) for image_path in image_paths]

    mean_pixel_values, centered_dataset = standarized_dataset(processed_images)

    eigenvectors, projected_dataset = set_pca(centered_dataset)

    query_path = "../test/query.jpg"
    query_vector = load_and_process_image(query_path, dataset=False)

    projected_query_vector = project_to_pca(query_vector, mean_pixel_values, eigenvectors)

    similarities = compute_euclidean_distance(projected_query_vector, projected_dataset)

    top_n = 10
    for idx, dist in similarities[:top_n]:
        print(f"Gambar {image_paths[idx]} dengan jarak: {dist}")

    end = time.time()
    print(end - start)