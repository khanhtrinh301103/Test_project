import os
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from skimage.feature import hog  # Thư viện để trích xuất đặc trưng HOG
from PIL import Image  # Sử dụng Pillow để xử lý nhiều định dạng ảnh

# Đường dẫn đến dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), '../dataset')

# Khởi tạo mô hình KNN
knn_model = None
label_encoder = None

# Hàm để trích xuất đặc trưng HOG từ ảnh
def extract_features(image):
    features, _ = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    return features

# Hàm để load dataset và huấn luyện mô hình
def load_and_train_model():
    global knn_model, label_encoder
    images = []
    labels = []

    # Duyệt qua tất cả các thư mục con trong dataset (các loại thời tiết)
    for weather_type in os.listdir(DATASET_PATH):
        weather_folder = os.path.join(DATASET_PATH, weather_type)
        if os.path.isdir(weather_folder):
            # Duyệt qua từng ảnh trong thư mục thời tiết
            for img_file in os.listdir(weather_folder):
                img_path = os.path.join(weather_folder, img_file)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Đọc ảnh dưới dạng grayscale

                # Kiểm tra xem ảnh có được đọc đúng hay không
                if img is None:
                    print(f"Error: Could not read image {img_path}, skipping...")
                    continue

                img_resized = cv2.resize(img, (100, 100))  # Resize ảnh về kích thước 100x100
                features = extract_features(img_resized)  # Trích xuất đặc trưng
                images.append(features)  # Thêm đặc trưng vào danh sách
                labels.append(weather_type)  # Gán nhãn là loại thời tiết

    # Chuyển labels sang dạng số
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)

    # Khởi tạo mô hình KNN
    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(images, labels)
    print("Model training complete.")

# Hàm xử lý hình ảnh người dùng tải lên và trả về loại thời tiết
def process_user_image(image):
    global knn_model, label_encoder

    if knn_model is None or label_encoder is None:
        load_and_train_model()  # Huấn luyện mô hình nếu chưa có

    # Đọc ảnh người dùng và chuyển đổi về định dạng RGB, xử lý nhiều định dạng ảnh
    try:
        img_pil = Image.open(image)  # Sử dụng Pillow để mở ảnh với nhiều định dạng khác nhau
        img_pil = img_pil.convert('L')  # Chuyển ảnh sang grayscale
        img = np.array(img_pil)  # Chuyển ảnh thành mảng numpy
    except Exception as e:
        return f"Error: Could not process the uploaded image. Details: {str(e)}"

    # Kiểm tra kích thước của ảnh
    if img.size == 0:
        return "Error: The uploaded image is empty."

    img_resized = cv2.resize(img, (100, 100))  # Resize ảnh về kích thước 100x100
    features = extract_features(img_resized)  # Trích xuất đặc trưng
    features = features.reshape(1, -1)  # Chuẩn bị dữ liệu để đưa vào mô hình

    # Dự đoán loại thời tiết
    prediction = knn_model.predict(features)
    weather_type = label_encoder.inverse_transform(prediction)[0]  # Chuyển nhãn số thành tên thời tiết

    return f"The weather in the image is: {weather_type}"
