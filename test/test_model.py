import os
import librosa
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
import librosa.display
import uuid

# ================== Cấu hình ===================
MODEL_PATH = "./model/efficientnet_model.tflite"
IMG_SIZE = 224
NUM_CLASSES = 3
TEMP_IMG_DIR = "./temp_images"  # Thư mục tạm để lưu ảnh spectrogram
os.makedirs(TEMP_IMG_DIR, exist_ok=True)

# ================== Hàm xử lý ===================
def split_wav_to_segments(folder_path, segment_duration=30):
    result = {}
    index = 0

    for filename in os.listdir(folder_path):
        if not filename.endswith(".wav"):
            continue

        file_path = os.path.join(folder_path, filename)
        print(f"🔄 Đang xử lý: {file_path}")

        try:
            y, sr = librosa.load(file_path, sr=None)
        except Exception as e:
            print(f"❌ Lỗi: {filename} ({str(e)}). Xóa...")
            try:
                os.remove(file_path)
            except:
                pass
            continue

        segment_samples = segment_duration * sr
        total_samples = len(y)
        num_segments = total_samples // segment_samples
        base_filename = os.path.splitext(filename)[0]

        if num_segments == 0:
            print(f"⚠️ Quá ngắn, bỏ: {filename}")
            continue

        for i in range(num_segments):
            start = int(i * segment_samples)
            end = int(start + segment_samples)
            segment = y[start:end]

            new_filename = f"{base_filename}_part{i+1}.wav"
            new_path = os.path.join(folder_path, new_filename)
            sf.write(new_path, segment, sr)
            print(f"✅ Đã lưu: {new_filename}")
            result[index] = {"dir": new_path}
            index += 1

        try:
            os.remove(file_path)
        except:
            pass

    return result


def load_samples(samples_listdir, duration=30):
    for index, sample in samples_listdir.items():
        file_path = sample["dir"]
        y, sr = librosa.load(file_path, sr=None)

        target_length = duration * sr
        if len(y) > target_length:
            start = np.random.randint(0, len(y) - target_length)
            y = y[start:start + target_length]
        else:
            y = np.pad(y, (0, max(0, target_length - len(y))))
        samples_listdir[index]["sampling"] = y
        samples_listdir[index]["sr"] = sr
    return samples_listdir


def get_mel_spectrogram(samples):
    for index, item in samples.items():
        y = item["sampling"]
        sr = item["sr"]
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        S_db = librosa.amplitude_to_db(S, ref=np.max)
        samples[index]["mel-spec-db"] = S_db
    return samples


def save_spectrogram_as_image(S_db, index, out_dir=TEMP_IMG_DIR):
    fig = plt.figure(figsize=(3, 3))
    librosa.display.specshow(S_db, sr=22050, x_axis=None, y_axis=None, cmap='magma')
    plt.axis('off')

    file_name = f"{uuid.uuid4().hex}_{index}.png"
    img_path = os.path.join(out_dir, file_name)

    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return img_path


def preprocess_image(image_path, img_size=224):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((img_size, img_size))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_image(img_array):
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    predicted_class = int(np.argmax(output_data))
    confidence = float(np.max(output_data))
    return predicted_class, confidence


# ================== Chạy pipeline ===================
if __name__ == "__main__":
    folder_path = "./data_test"
    
    # B1. Cắt WAV
    samples = split_wav_to_segments(folder_path)
    
    # B2. Load samples
    samples = load_samples(samples)
    
    # B3. Mel-spectrogram
    samples = get_mel_spectrogram(samples)

    # B4. Dự đoán từng mẫu
    for index, sample in samples.items():
        print(f"\n🎵 Dự đoán sample {index}:")

        # Lưu spectrogram thành ảnh
        img_path = save_spectrogram_as_image(sample["mel-spec-db"], index)

        # Tiền xử lý ảnh
        input_data = preprocess_image(img_path, IMG_SIZE)

        # Dự đoán
        predicted_class, confidence = predict_image(input_data)

        print(f"🧠 Dự đoán lớp: {predicted_class}")
        print(f"✅ Độ tin cậy: {round(confidence * 100, 2)}%")
