import numpy as np # Numerical Python
import mido # MIDI Objects for Python
import os
import time

# 1. Pemrosesan Audio, Normalisasi Pitch, dan Windowing, fokus pada track melodi utama di Channel 1
def load_midi_file(file_path, channel = 1):
    
    # membaca MIDI file dengan library mido (MIDI file consist of track, pesan MIDI, dan metadata)
    midi = mido.MidiFile(file_path) 
    
    # list kosong yang akan diisi dengan note-note melodi dari Channel 1
    melody = [] 
    
    # iterasi setiap track dalam MIDI file dengan setiap MIDI file dapat berisi beberapa track (contohnya melodi utama, harmoni, drum, dsb)
    for track in midi.tracks:

        # iterasi setiap pesan MIDI dalam track (contohnya perubahan tempo, note, kontrol instrumen, dsb)
        for msg in track:

            # jika pesan MIDI adalah note_on (note dimainkan) dan pada Channel 1 (MIDI menggunakan indeks berbasis 0)
            if msg.type == 'note_on' and msg.channel == channel - 1:

                # tambahkan note (setiap note mewakili tinggi nada tertentu) ke list melody
                melody.append(msg.note)
    
    # kondisi apabila note pada channel 1 kosong
    if len(melody) == 0:
        raise ValueError(f"File MIDI {file_path} tidak memiliki note pada channel {channel}.")

    return np.array(melody)

def normalize_pitch(notes):

    mean_pitch = np.mean(notes)
    
    # menghitung standar deviasi pitch dari notes
    std_pitch = np.std(notes)
    if std_pitch == 0:
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

    
    # menggabungkan pitch dan durasi
    combined = np.column_stack((normalized_pitch[:-1], normalized_durations))
    
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

    # return histogram kosong jika tidak ada notes
    if len(notes) == 0:
        return np.zeros(128)  

    # jika sum=0, return langsung tanpa normalisasi
    hist, _ = np.histogram(notes, bins=128, range=(0, 127))
    if np.sum(hist) == 0:
        return hist 
    
    # normalisasi
    hist = hist / np.sum(hist)
    return hist

def compute_histogram_relative(notes):

    # tidak cukup data untuk menghitung perbedaan, return histogram kosong
    if len(notes) <= 1:  
        return np.zeros(255) 
    
    # menghitung perbedaan antar notes
    differences = np.diff(notes)
    hist, _ = np.histogram(differences, bins=255, range=(-127, 127))
    
    # jika sum=0, return langsung tanpa normalisasi
    if np.sum(hist) == 0:
        return hist
    
    # normalisasi
    hist = hist / np.sum(hist)
    return hist

def compute_histogram_first(notes):

    # tidak ada notes, return histogram kosong
    if len(notes) == 0: 
        return np.zeros(255)

    # menghitung perbedaan terhadap note pertama
    first_note = notes[0]
    differences = notes - first_note
    hist, _ = np.histogram(differences, bins=255, range=(-127, 127))
    
    # jika sum=0, return langsung tanpa normalisasi
    if np.sum(hist) == 0:
        return hist
    
    # normalisasi
    hist = hist / np.sum(hist)
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
    
    dot_product = np.dot(hist1, hist2)
    magnitude_hist1 = sum(a**2 for a in hist1)**0.5
    magnitude_hist2 = sum(b**2 for b in hist2)**0.5

    if magnitude_hist1 == 0 or magnitude_hist2 == 0:
        return 0

    return dot_product / (magnitude_hist1 * magnitude_hist2)

def find_most_similar_midi(query_midi_path, processed_audios):
    
    try:
        query_notes = load_midi_file(query_midi_path)
        query_hist_atb = compute_histogram_absolute(query_notes)
        query_hist_rtb = compute_histogram_relative(query_notes)
        query_hist_ftb = compute_histogram_first(query_notes)
    except Exception as e:
        print(f"Error memproses file query MIDI: {e}")
        return None

    # iterasi semua file MIDI dalam dataset untuk mencari tingkat kemiripan
    distances = []
    
    for i, vectors in enumerate(processed_audios):
        
        # ekstraksi histogram untuk database MIDI
        db_hist_atb = compute_histogram_absolute(vectors)
        db_hist_rtb = compute_histogram_relative(vectors)
        db_hist_ftb = compute_histogram_first(vectors)

        # hitung similaritas
        sim_atb = cosine_similarity(query_hist_atb, db_hist_atb)
        sim_rtb = cosine_similarity(query_hist_rtb, db_hist_rtb)
        sim_ftb = cosine_similarity(query_hist_ftb, db_hist_ftb)

        # agregasi skor similaritas
        total_similarity = (0.4 * sim_atb) + (0.3 * sim_rtb) + (0.3 * sim_ftb)

        distances.append((i, total_similarity))

    # Urutkan berdasarkan jarak terkecil
    distances.sort(key=lambda x: x[1], reverse=True)
    
    return distances

if __name__ == "__main__":
    
    start = time.time()
    
    query_file = "../test/query.mid"
    dataset_audios = "../test/audios"

    processed_audios = []
    audio_names = []
    for root, _, files in os.walk(dataset_audios):
        for file in files:
            if file.endswith('.mid') or file.endswith('.midi'):
                    audio_names.append(file)
                    file_path = os.path.join(root, file)
                    try:
                        db_notes = load_midi_file(file_path)
                        processed_audios.append(db_notes)
                    except Exception as e:
                        print(f"Gagal memproses file {file_path}: {e}")

    similarities = find_most_similar_midi(query_file, processed_audios)

    
    i = 1
    for idx, value in similarities:
        print(f"{i}. Audio {audio_names[idx]} dengan nilai kemiripan: {value}")
        i += 1
        if (value < 0.8):
            break

    end = time.time()
    print(end - start)