🚦 Traffic Sign Detection and Explanation

Toàn bộ source code của chương trình được đăng trên GitHub: https://github.com/kaiz0708/detech-explain-traffic-sign-TLCN

📥 Cài đặt và Chạy Demo
Để cài đặt chương trình, sử dụng lệnh sau hoặc tải code từ repository: git clone https://github.com/kaiz0708/detech-explain-traffic-sign-TLCN.git

📦 Yêu cầu Thư Viện
Để chạy chương trình, cài đặt các thư viện Python sau:
Flask: Tạo server và giao diện web.
dotenv và os: Quản lý biến môi trường.
openai: Tương tác với API OpenAI.
cv2 và numpy: Xử lý ảnh.
ultralytics: Triển khai YOLO (object detection).
torch: Thư viện học sâu.
pandas và matplotlib: Phân tích và trực quan hóa dữ liệu.
zipfile: Làm việc với file nén.

📂 Tài Nguyên Bổ Sung
Vui lòng tải các file dataset và mô hình và lấy API_KEY của OPEN AI tại đường link sau:

https://drive.google.com/drive/folders/1AFkcHa_9TF2WJTkkY7ZwFNmDjO70BirI?usp=sharing

🛠️ Cấu Trúc Source Code

detech-explain-traffic-sign-TLCN/
│
├── app.py                  # File chính để chạy server Flask
├── best_model_yolov8m.pt   # File mô hình YOLO đã được train
├── config.yaml             # File cấu hình
├── solve_img.py            # Xử lý ảnh đầu vào
├── Yolov8_training.ipynb   # Notebook train YOLOv8
├── static/                 # Thư mục chứa file tĩnh (CSS, JS, hình ảnh)
├── templates/              # Thư mục chứa giao diện HTML
├── .env                    # File môi trường (chứa API_KEY)
└── dataset.zip             # Dữ liệu huấn luyện


🚀 Chạy Chương Trình
Sau khi cài đặt đầy đủ, chạy lệnh sau để khởi động server: python app.py


Mở trình duyệt và truy cập vào: http://127.0.0.1:5000/

🎉 Chúc bạn thành công!
