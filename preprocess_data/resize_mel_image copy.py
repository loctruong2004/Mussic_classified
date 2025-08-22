from PIL import Image
import os

def resize_all_images(source_folder, target_folder, target_size=(224, 224)):
    """
    Resize tất cả ảnh .png hoặc .jpg từ source_folder và lưu sang target_folder,
    giữ nguyên cấu trúc thư mục con.
    """
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                source_path = os.path.join(root, file)

                # Tạo đường dẫn đích tương ứng trong thư mục mới
                relative_path = os.path.relpath(source_path, source_folder)
                target_path = os.path.join(target_folder, relative_path)

                # Tạo thư mục đích nếu chưa tồn tại
                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                try:
                    img = Image.open(source_path).convert("RGB")
                    img = img.resize(target_size)
                    img.save(target_path)
                    print(f"✅ Resized & saved: {target_path}")
                except Exception as e:
                    print(f"❌ Error resizing {source_path}: {e}")
