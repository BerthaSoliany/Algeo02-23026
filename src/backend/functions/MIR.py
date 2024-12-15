import numpy as np
import mido # MIDI Objects for Python
import os
import time

def fix_invalid_bytes(file_path, output_path):
    try:
        midi = mido.MidiFile(file_path)
        for i, track in enumerate(midi.tracks):
            for msg in track:
                if hasattr(msg, 'data'):
                    corrected_data = []
                    for byte in msg.data:
                        if byte < 0:
                            corrected_data.append(0)  # replace invalid byte with 0
                        elif byte > 127:
                            corrected_data.append(127)  # replace invalid byte with 127
                        else:
                            corrected_data.append(byte)
                    msg.data = corrected_data
        midi.save(output_path)
        print(f"Fixed MIDI file saved to {output_path}")
    except Exception as e:
        print(f"Error while fixing file {file_path}: {e}")

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

def load_midi_file_considering_channels(file_path):
    
    # Membaca file MIDI dengan library mido
    midi = mido.MidiFile(file_path)

    # Dictionary untuk menyimpan jumlah note per channel di setiap track
    channel_note_counts = {}

    # Iterasi setiap track dalam file MIDI
    for track in midi.tracks:
        
        # Iterasi setiap pesan MIDI dalam track
        for msg in track:
            
            # Cek jika pesan MIDI adalah 'note_on'
            if msg.type == 'note_on':
                
                # Ambil channel dari pesan
                channel = msg.channel

                # Jika channel belum ada dalam dictionary, buat entry baru
                if channel not in channel_note_counts:
                    channel_note_counts[channel] = []
                
                # Tambahkan note ke list untuk channel yang sesuai
                channel_note_counts[channel].append(msg.note)

    # Cari channel dengan jumlah note terbanyak
    max_channel = max(channel_note_counts, key=lambda x: len(channel_note_counts[x]))

    # Mengambil note dengan jumlah terbanyak
    return np.array(channel_note_counts[max_channel])

def load_midi_file_considering_duration(file_path, main_channel=None):
    midi = mido.MidiFile(file_path)
    channel_durations = {}
    
    for track in midi.tracks:
        active_notes = {}
        current_time = 0
        
        for msg in track:
            current_time += msg.time
            
            if msg.type == 'note_on' and msg.velocity > 0:
                channel = msg.channel
                active_notes.setdefault(channel, []).append(current_time)
                
            elif msg.type in ['note_off', 'note_on'] and msg.velocity == 0:
                channel = msg.channel
                if channel in active_notes and active_notes[channel]:
                    start_time = active_notes[channel].pop(0)
                    duration = current_time - start_time
                    channel_durations[channel] = channel_durations.get(channel, 0) + duration
    
    if main_channel is None:
        if channel_durations:
            main_channel = max(channel_durations, key=channel_durations.get)
            print(f"Longest active channel: {main_channel + 1}")
        else:
            raise ValueError(f"No active channels found in {file_path}.")

    melody = []
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.channel == main_channel and msg.velocity > 0:
                melody.append(msg.note)
    
    if not melody:
        raise ValueError(f"File {file_path} has no notes in channel {main_channel + 1}.")

    return np.array(melody)

def load_midi_file_considering_main_channel(file_path):
    def find_main_channel(file_path):
        midi = mido.MidiFile(file_path)
        for track in midi.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.channel == 0:
                    return 0
        potential_main_channels = []
        fallback_channels = []
        for track in midi.tracks:
            channel_data = {}
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    channel = msg.channel
                    pitch = msg.note
                    if channel not in channel_data:
                        channel_data[channel] = {"notes": 0, "pitches": []}
                    channel_data[channel]["notes"] += 1
                    channel_data[channel]["pitches"].append(pitch)
            for channel, data in channel_data.items():
                notes = data["notes"]
                pitch_range = (min(data["pitches"]) if data["pitches"] else None, 
                               max(data["pitches"]) if data["pitches"] else None)
                if notes > 50 and pitch_range[0] >= 60 and pitch_range[1] <= 80:
                    potential_main_channels.append((channel, notes, pitch_range))
                else:
                    fallback_channels.append((channel, notes, pitch_range))
        if potential_main_channels:
            best_channel = max(potential_main_channels, key=lambda x: x[1])
            return best_channel[0]
        elif fallback_channels:
            best_channel = max(fallback_channels, key=lambda x: x[1])
            return best_channel[0]
        else:
            raise ValueError("No main channel found.")
    try:
        main_channel = find_main_channel(file_path)
        return load_midi_file(file_path, channel=main_channel + 1)
    except Exception as e:
        raise ValueError(f"Error processing {file_path}: {e}")

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
    
    query_folder = "../query_files"
    query_file = os.path.join(query_folder, os.listdir(query_folder)[0])
    dataset_audios = "../extracted_datasets"

    processed_audios = []
    audio_names = []
    for root, _, files in os.walk(dataset_audios):
        for file in files:
            if file.endswith('.mid') or file.endswith('.midi'):
                    audio_names.append(file)
                    file_path = os.path.join(root, file)
                    fixed_file_path = os.path.join(root, f"fixed_{file}")
                    try:
                        fix_invalid_bytes(file_path, file_path)
                        db_notes = load_midi_file_considering_main_channel(file_path)
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