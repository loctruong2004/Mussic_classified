import os
import librosa as lb
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from unidecode import unidecode
import cv2
import shutil 
class_names = ['bolero', 'danca', 'pop']
img_height,img_width=225,225

model = load_model(r'D:\classified_music\check_point_resnet\best_model_epoch_02_acc_0.70.keras')
# Hàm xử lý STFT
def get_fft(samples, n_fft=2048, hop_length=512):
    for index, item in samples.items():
        D = np.abs(lb.stft(item["sampling"], n_fft=n_fft, hop_length=hop_length))
        samples[index]["stft"] = D
    return samples

# Hàm xử lý mel spectrogram
def get_mel_spectrogram(samples, sr=22050):
    for index, item in samples.items():
        S = lb.feature.melspectrogram(y=item["sampling"], sr=sr)
        S_db = lb.amplitude_to_db(S, ref=np.max)
        samples[index]["mel-spec-db"] = S_db
    return samples

# Hàm lưu ảnh mel spectrogram
def save_mel_spec(samples, root):
    image_paths = []
    for index, item in samples.items():
        S_db = item["mel-spec-db"]
        os.makedirs(root, exist_ok=True)

        # file_name = os.path.splitext(os.path.basename(item["dir"]))[0]
        file_name = unidecode(os.path.splitext(os.path.basename(item["dir"]))[0])
        out_path = os.path.join(root, file_name + ".png")
        plt.imsave(out_path, S_db)
        image_paths.append(out_path)
    return image_paths

# Hàm chính: predict và sinh ảnh spectrogram
def predict(file_path, duration=30):
    try:
        y, sr = lb.load(file_path, sr=None)
    except Exception as e:
        print(f"❌ Lỗi khi load: {file_path} ({e})")
        return

    segment_samples = duration * sr
    total_samples = len(y)
    num_segments = total_samples // segment_samples
    base_filename = os.path.splitext(os.path.basename(file_path))[0]

    if num_segments == 0:
        return

    # Tự động lấy class từ folder cha (ví dụ: 'pop')
    folder_path = os.path.dirname(file_path)

    # Folder lưu wav đã cắt
    output_folder = os.path.join(folder_path, "predict")
    os.makedirs(output_folder, exist_ok=True)

    samples = {}

    for i in range(num_segments):
        start = i * segment_samples
        end = start + segment_samples
        segment = y[start:end]

        new_filename = f"{base_filename}_part{i+1}.wav"
        new_path = os.path.join(output_folder, new_filename)

        sf.write(new_path, segment, sr)
        samples[i] = {
            "dir": new_path,
            "sampling": segment
        }

    samples = get_fft(samples)
    samples = get_mel_spectrogram(samples, sr)

    mel_root = os.path.join(output_folder, "mel-images")
    os.makedirs(mel_root, exist_ok=True)

    list_test = save_mel_spec(samples, mel_root)

    # === DỰ ĐOÁN TỪ ẢNH MEL ===
    print("\n🔍 Đang dự đoán")
    for path in list_test:
      image=cv2.imread(str(path))
      image_resized= cv2.resize(image, (img_height,img_width))
      image=np.expand_dims(image_resized,axis=0)
      predictions = model.predict(image)
      output_class=class_names[np.argmax(predictions)]
      confidences = predictions[0]
      predicted_index = np.argmax(confidences)
      confidence_score = confidences[predicted_index]
      print(f"The predicted binz{i} is {output_class} : {confidence_score:.2%}")
    try:
        shutil.rmtree(output_folder)
    except  Exception as e:
         print(f"\n Không thể xoá thư mục: {output_folder} ({e})")

predict(r"D:\classified_music\data_test\NeoDauBenQue-LuongGiaHuy-5288584.mp3")