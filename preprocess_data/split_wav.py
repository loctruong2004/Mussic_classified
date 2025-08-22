import os
import librosa
import soundfile as sf

def split_wav_to_segments(folder_path, segment_duration=30):
    """
    Chia các file .wav trong thư mục thành các đoạn nhỏ dài segment_duration (giây).
    Bỏ qua file đã cắt (_part), và xóa file lỗi khi gặp lỗi đọc.
    """
    for filename in os.listdir(folder_path):
        if not filename.endswith(".wav"):
            continue
        if "_part" in filename:
            # print(f"⏭️ Bỏ qua (đã cắt): {filename}")
            continue

        file_path = os.path.join(folder_path, filename)
        print(f"Đang xử lý: {file_path}")

        try:
            # Load file âm thanh
            y, sr = librosa.load(file_path, sr=None)
        except Exception as e:
            print(f" Lỗi khi load: {filename} ({str(e)}). Đang xóa file...")
            try:
                os.remove(file_path)
                print(f"🗑️ Đã xóa file lỗi: {filename}\n")
            except Exception as delete_error:
                print(f"⚠️ Không thể xóa file: {filename} ({delete_error})\n")
            continue

        segment_samples = segment_duration * sr
        total_samples = len(y)
        num_segments = total_samples // segment_samples
        base_filename = os.path.splitext(filename)[0]

        if num_segments == 0:
            print(f"⚠️ File ngắn hơn {segment_duration} giây, bỏ qua: {filename}\n")
            continue

        # Cắt và lưu các đoạn
        for i in range(num_segments):
            start = int(i * segment_samples)
            end = int(start + segment_samples)
            segment = y[start:end]

            new_filename = f"{base_filename}_part{i+1}.wav"
            new_path = os.path.join(folder_path, new_filename)
            sf.write(new_path, segment, sr)
            print(f"✅ Đã lưu: {new_filename}")

        # Xóa file gốc sau khi cắt xong
        try:
            os.remove(file_path)
            print(f"🗑️ Đã xóa file gốc: {filename}\n")
        except Exception as e:
            print(f"⚠️ Không thể xóa file gốc: {filename} ({str(e)})\n")

# # Ví dụ: thay đổi đường dẫn thư mục WAV tại đây
folder_path_cheo = r"D:\classified_music\data\cheo"
folder_path_remix = r"D:\classified_music\data\remix"
folder_path_bolero = r"D:\classified_music\data\bolero"
folder_path_cailuong = r"D:\classified_music\data\cailuong"
folder_path_danca = r"D:\classified_music\data\danca"
folder_path_pop = r"D:\classified_music\data\pop"
# split_wav_to_segments(folder_path_cheo)
split_wav_to_segments(folder_path_remix)
# split_wav_to_segments(folder_path_cailuong)
split_wav_to_segments(folder_path_bolero)
# split_wav_to_segments(folder_path_danca)
split_wav_to_segments(folder_path_pop)

