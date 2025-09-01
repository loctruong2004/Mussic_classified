# Mussic_classified
# 🎵 Music Classification using Deep Learning

## 📌 Giới thiệu

Dự án **Mussic_classified** tập trung vào việc **phân loại nhạc** dựa trên file âm thanh `.wav`.  
Ý tưởng chính:
- Biến đổi tín hiệu âm thanh thành **Mel-Spectrogram** (dạng ảnh).
- Huấn luyện mô hình học sâu dựa trên ảnh này bằng nhiều kiến trúc CNN khác nhau:  
  - CNN cơ bản  
  - ResNet-50  
  - EfficientNet-B0  

Mục tiêu: So sánh hiệu năng của các kiến trúc khác nhau và xây dựng mô hình dự đoán chính xác thể loại nhạc.

---

## 📂 Cấu trúc dự án
```
Mussic_classified/
├── README.md # Tài liệu dự án
├── requirement.txt # Danh sách dependencies
├── preprocess_data/ # Script/notebook tiền xử lý dữ liệu
├── train_with_model1.ipynb # Huấn luyện với CNN cơ bản
├── train_with_resnet.ipynb # Huấn luyện với ResNet-50
├── Train_with_EfficientNetB0.ipynb # Huấn luyện với EfficientNet-B0
├── train_with_pytorch.ipynb # Huấn luyện mô hình bằng PyTorch
├── use_model.ipynb # Thử nghiệm & đánh giá mô hình
└── test/ # Dữ liệu kiểm thử
```
---

## ⚙️ Cài đặt

1. Clone repository:
   ```bash
   git clone https://github.com/loctruong2004/Mussic_classified.git
   cd Mussic_classified
   ```
2.Tạo môi trường ảo (khuyến nghị):
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # trên Linux/Mac
  venv\Scripts\activate     # trên Windows
   ```
3.Cài đặt dependencies:
  ```bash
  pip install -r requirement.txt
  ```
🚀 Quy trình thực hiện
<img width="827" height="502" alt="image" src="https://github.com/user-attachments/assets/627b7f26-2bfa-4f89-b8fe-46a25f2cb979" />

Tiền xử lý dữ liệu

Chạy script trong preprocess_data/ để chuyển file .wav → mel spectrogram.

Dữ liệu đầu ra là ảnh, được dùng làm input cho mô hình.

Huấn luyện mô hình

train_with_model1.ipynb: CNN cơ bản.

train_with_resnet.ipynb: ResNet-50.

Train_with_EfficientNetB0.ipynb: EfficientNet-B0.

train_with_pytorch.ipynb: Demo huấn luyện với PyTorch.

Đánh giá & sử dụng mô hình

use_model.ipynb để load mô hình đã huấn luyện, dự đoán và đánh giá độ chính xác.

Có thể tính accuracy, confusion matrix, loss/accuracy curve,...


