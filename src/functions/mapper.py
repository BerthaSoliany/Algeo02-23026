import os
import json

def generate_mapper_json(images_folder, audios_folder, output_file):
    # Pastikan folder ada
    if not os.path.exists(images_folder):
        print(f"Error: Folder {images_folder} does not exist.")
        return
    
    if not os.path.exists(audios_folder):
        print(f"Error: Folder {audios_folder} does not exist.")
        return

    # Ambil file dari folder
    images = sorted([f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))])
    audios = sorted([f for f in os.listdir(audios_folder) if os.path.isfile(os.path.join(audios_folder, f))])

    # Pastikan ada file di kedua folder
    if not images or not audios:
        print("Error: One of the folders is empty.")
        return

    # Buat data mapper (gunakan gambar berulang jika jumlah audio lebih banyak)
    mapper_data = []
    for i, audio in enumerate(audios):
        pic_name = images[i % len(images)]  # Circular mapping
        mapper_data.append({"audio_file": audio, "pic_name": pic_name})

    # Tulis ke file JSON
    with open(output_file, 'w') as mapper_file:
        json.dump(mapper_data, mapper_file, indent=4)  # Menyimpan dengan indentasi 4 untuk keterbacaan

    print(f"Mapper file '{output_file}' generated successfully.")
