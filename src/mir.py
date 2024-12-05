import numpy as np # Numerical Python
import mido # MIDI Objects for Python
from scipy.spatial.distance import cosine # Cosine similarity (NANTI DIUBAH PLS JANGAN PAKE LIBRARY!!!)
import os

# 1. Pemrosesan Audio, Normalisasi Pitch, dan Windowing
def load_midi_file(file_path, channel = 1): # fokus pada track melodi utama di Channel 1
    midi = mido.MidiFile(file_path) # membaca MIDI file dengan library mido (MIDI file consist of track, pesan MIDI, dan metadata)
    
    melody = [] # list kosong yang akan diisi dengan note-note melodi dari Channel 1
    
    for track in midi.tracks: # iterasi setiap track dalam MIDI file dengan setiap MIDI file dapat berisi beberapa track (contohnya melodi utama, harmoni, drum, dsb)
        for msg in track: # iterasi setiap pesan MIDI dalam track (contohnya perubahan tempo, note, kontrol instrumen, dsb)
            if msg.type == 'note_on' and msg.channel == channel - 1: # jika pesan MIDI adalah note_on (note dimainkan) dan pada Channel 1 (MIDI menggunakan indeks berbasis 0)
                melody.append(msg.note) # tambahkan note (setiap note mewakili tinggi nada tertentu) ke list melody

    if len(melody) == 0:
        raise ValueError(f"File MIDI {file_path} tidak memiliki note pada channel {channel}.") # INI NANTI HARUS DICARI-CARI DONG ANJIR CHANNEL UTAMANYA APA ONE BY ONE ANJGGGGGGGG

    return np.array(melody) # mengembalikan list melody dalam bentuk array NumPy

def normalize_pitch(notes):
    mean_pitch = np.mean(notes) # menghitung rata-rata pitch dari notes
    std_pitch = np.std(notes) # menghitung standar deviasi pitch dari notes
    if std_pitch == 0:  # handle perhitungan standar deviasi 0 (semua note sama)
        return np.zeros_like(notes)
    return (notes - mean_pitch) / std_pitch

def normalize_tempo_and_pitch(notes, times):
    normalized_pitch = normalize_pitch(notes)
    durations = np.diff(times)
    mean_duration = np.mean(durations)
    std_duration = np.std(durations)
    
    if std_duration == 0:
        normalized_durations = np.zeros_like(durations)
    else:
        normalized_durations = (durations - mean_duration) / std_duration
    
    combined = np.column_stack((normalized_pitch[:-1], normalized_durations)) # menggabungkan pitch dan durasi
    
    return combined

def windowing_with_normalization(notes, times, window_size=20, step_size=4):
    combined_features = normalize_tempo_and_pitch(notes, times)
    windows = []
    
    for i in range(0, len(combined_features) - window_size + 1, step_size):
        window = combined_features[i:i + window_size]
        windows.append(window)
    
    return windows

# 2. Ekstraksi Fitur
# 2.1 Distribusi Tone
def compute_histogram_absolute(notes):
    if len(notes) == 0:
        return np.zeros(128)  # return histogram kosong jika tidak ada notes

    hist, _ = np.histogram(notes, bins=128, range=(0, 127))
    if np.sum(hist) == 0:
        return hist  # jika sum=0, return langsung tanpa normalisasi
    
    hist = hist / np.sum(hist)  # normalisasi
    return hist

def compute_histogram_relative(notes):
    if len(notes) <= 1:  # tidak cukup data untuk menghitung perbedaan
        return np.zeros(255)  # histogram kosong
    
    differences = np.diff(notes)  # menghitung perbedaan antar notes
    hist, _ = np.histogram(differences, bins=255, range=(-127, 127))
    
    if np.sum(hist) == 0:  # jika sum=0, return langsung tanpa normalisasi
        return hist
    
    hist = hist / np.sum(hist)  # normalisasi
    return hist

def compute_histogram_first(notes):
    if len(notes) == 0:  # tidak ada notes
        return np.zeros(255)  # histogram kosong

    first_note = notes[0]
    differences = notes - first_note  # menghitung perbedaan terhadap note pertama
    hist, _ = np.histogram(differences, bins=255, range=(-127, 127))
    
    if np.sum(hist) == 0:  # jika sum=0, return langsung tanpa normalisasi
        return hist
    
    hist = hist / np.sum(hist)  # normalisasi
    return hist

# 2.2. Normalisasi
def normalize_histogram(histogram):
    total = np.sum(histogram)
    if total == 0:
        return histogram
    normalized_histogram = histogram / total
    return normalized_histogram

# 3. Perhitungan Similaritas
def cosine_similarity(hist1, hist2):
    return 1 - cosine(hist1, hist2)  # menghitung Cosine similarity

def main():
    midi_path_query = "query_midi_file.mid"  # Path untuk file MIDI query
    midi_path_database = "database_midi_file.mid"  # Path untuk file MIDI database

    # Load dan normalisasi note dari file MIDI
    try:
        query_notes = load_midi_file(midi_path_query)
        db_notes = load_midi_file(midi_path_database)
    except Exception as e:
        print(f"Error saat memproses file MIDI: {e}")
        return

    query_norm = normalize_pitch(query_notes)
    db_norm = normalize_pitch(db_notes)

    # Ekstraksi fitur histogram
    query_hist_atb = compute_histogram_absolute(query_norm)
    query_hist_rtb = compute_histogram_relative(query_norm)
    query_hist_ftb = compute_histogram_first(query_norm)

    db_hist_atb = compute_histogram_absolute(db_norm)
    db_hist_rtb = compute_histogram_relative(db_norm)
    db_hist_ftb = compute_histogram_first(db_norm)

    # Hitung similaritas menggunakan cosine similarity manual
    sim_atb = cosine_similarity_manual(query_hist_atb, db_hist_atb)
    sim_rtb = cosine_similarity_manual(query_hist_rtb, db_hist_rtb)
    sim_ftb = cosine_similarity_manual(query_hist_ftb, db_hist_ftb)

    # Agregasi skor similaritas dengan bobot
    total_similarity = (0.4 * sim_atb) + (0.3 * sim_rtb) + (0.3 * sim_ftb)

    # Output hasil
    print(f"Cosine Similarity:\nATB: {sim_atb:.4f}, RTB: {sim_rtb:.4f}, FTB: {sim_ftb:.4f}")
    print(f"Total Similarity Score: {total_similarity:.4f}")

def find_most_similar_midi(query_midi_path, dataset_folder):
    try:
        query_notes = load_midi_file(query_midi_path)
        query_hist_atb = compute_histogram_absolute(query_notes)
        query_hist_rtb = compute_histogram_relative(query_notes)
        query_hist_ftb = compute_histogram_first(query_notes)
    except Exception as e:
        print(f"Error memproses file query MIDI: {e}")
        return None

    # inisialisasi untuk pencarian file MIDI paling mirip
    max_similarity = -1
    most_similar_file = None

    # iterasi semua file MIDI dalam dataset
    for root, _, files in os.walk(dataset_folder):
        for file in files:
            if file.endswith('.mid') or file.endswith('.midi'):
                try:
                    file_path = os.path.join(root, file)
                    db_notes = load_midi_file(file_path)

                    # ekstraksi histogram untuk database MIDI
                    db_hist_atb = compute_histogram_absolute(db_notes)
                    db_hist_rtb = compute_histogram_relative(db_notes)
                    db_hist_ftb = compute_histogram_first(db_notes)

                    # hitung similaritas
                    sim_atb = cosine_similarity(query_hist_atb, db_hist_atb)
                    sim_rtb = cosine_similarity(query_hist_rtb, db_hist_rtb)
                    sim_ftb = cosine_similarity(query_hist_ftb, db_hist_ftb)

                    # agregasi skor similaritas
                    total_similarity = (0.4 * sim_atb) + (0.3 * sim_rtb) + (0.3 * sim_ftb)

                    # update jika ditemukan file dengan similaritas lebih tinggi
                    if total_similarity > max_similarity:
                        max_similarity = total_similarity
                        most_similar_file = file_path
                except Exception as e:
                    print(f"Error memproses file {file}: {e}")

    return most_similar_file, max_similarity

if __name__ == "__main__":
    query_file = r"C:\Users\User\Downloads\backstreetboy.mid"
    dataset_dir = r"C:\Users\User\Downloads\midi_file"

    try:
        result, similarity = find_most_similar_midi(query_file, dataset_dir)
        if result:
            print(f"File MIDI yang paling mirip: {result}")
            print(f"Skor Similaritas: {similarity:.4f}")
        else:
            print("Tidak ditemukan file yang mirip.")
    except Exception as e:
        print(f"Terjadi error: {e}")