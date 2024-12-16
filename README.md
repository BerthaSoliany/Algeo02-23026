# Algeo02-23026
> Tugas Besar 2 Aljabar Linear dan Geometri

<!-- foto logo -->
**<p align="center">Ikan dan Pisang</p>**
**<p align="center">Kelompok 35</p>**

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Features](#features)
- [SneakPeak](#sneakpeak)
- [Contributors](#contributors)


## About the Project
Program ini mempunyai dua jenis *information retrieval*, yakni *Image Retrieval* dan *Music Information Retrieval* . *Image Retrieval* adalah proses memasukkan input berupa gambar dan mendapatkan gambar serupa yang ada di dalam basis data berdasarkan informasi dan perhitungan tertentu. PCA digunakan untuk mengurangi dimensi data sehingga pencarian menjadi lebih efisien. *Music Information Retrieval* (MIR) adalah proses memasukkan input berupa audio dan mendapatkan audio yang sesuai di dalam basis data berdasarkan fitur dan analisis tertentu. Oleh karena itu, tujuan utama dari program adalah untuk melakukan pencarian gambar dan musik. 


## Getting Started
1. Clone Repository ini
    ```sh
    git clone https://github.com/BerthaSoliany/Algeo02-23026.git

2. Ubah directori menuju `src`
    ```sh
    cd src

3. Buat virtual enviroment
    ```sh
    python -m venv venv

4. Aktivasi virtual enviroment
  Untuk windows:
    ```sh
    venv\Scripts\activate
  Untuk Unix-like Shell:
    ```sh
    source venv\Scripts\activate

> [!NOTE]
> Sesuaikan kembali path dari activate sesuai dengan venv masing-masing

5. Install dependensi
    ```sh
    pip install -r requirements.txt

6. Jalankan app.py
    ```sh
    python app.py

7. Jalankan website
    ```sh
    npm run dev

8. Lakukan klik link yang muncul di terminal. Biasanya http://localhost:3000


# How to Use
1. Lakukan langkah di atas.
2. Setelah muncul tampilan *website* pada *web browser*, dapat dilakukan navigasi lewat menu bar. Program utama terdapat pada halaman `finder`.
3. Unggah album atau lagu yang ingin dicari kemiripannya.
4. Unggah dataset *audio* dan *image*.
5. Unggah *mapper* (opsional). Apabila tidak mengunggah mapper, program akan secara otomatis melakukan pemasangan secara acak
6. Klik tombol `process`. `AIR` untuk pencarian album dan `MIR` untuk pencarian lagu.
7. Tunggu sejenak sampai hasil ditampilkan.
8. Terdapat tombol `album` dan `music` pada bagian kanan yang berguna untuk melihat hasil pencarian.
9. Hasil yang ditampilkan berupa gambar, nama, dan persentase kemiripan. Untuk *audio* disediakan tombol untuk memutar musik. 


## Features
| Features | Status |
| --- | --- |
| Uploading | ✔ |
| Search Album | ✔ |
| Search Music | ✔ |
| Searching | ✔ |
| Auto-save | ✔ |
| Laporan | ✔ |
| Video | ✔ |


## Sneakpeak
### Halaman Home
1. Deskripsi singkat

2. Cara Penggunaan

3. Tentang proyek


### Halaman Finder
1. Tampilan awal

2. Error Message
- Ketika salah mengunggah tipe file

- Ketika Generate Auto Mapper

3. Tampilan unggah album/lagu

4. Tampilan unggahan lengkap


### Halaman About Us


### Lain-lain
- Random Generate Mapper

- Auto-save


<!-- foto bareng -->
## Contributors
| NIM | Nama |
| --- | --- |
| 13523026 | Bertha Soliany Frandi |
| 13523031 | Rafen Max Alessandro |
| 13523087 | Grace Evelyn Simon |
</br>

**<p align="center">Terima Kasih</p>**