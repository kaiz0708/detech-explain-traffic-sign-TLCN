<h1>🚦 Traffic Sign Detection and Explanation</h1>

<p>
Toàn bộ source code của chương trình được đăng trên GitHub: <br>
<a href="https://github.com/kaiz0708/detech-explain-traffic-sign-TLCN" target="_blank">
  <strong>👉 Xem Repository tại đây 👈</strong>
</a>
</p>

<h2>📥 Cài đặt và Chạy Demo</h2>
<p>Để cài đặt chương trình, sử dụng lệnh sau hoặc tải code từ repository:</p>

<pre>
git clone https://github.com/kaiz0708/detech-explain-traffic-sign-TLCN.git
</pre>

<h2>📦 Yêu cầu Thư Viện</h2>
<p>Để chạy chương trình, cài đặt các thư viện Python sau:</p>
<ul>
  <li><strong>Flask</strong>: Tạo server và giao diện web.</li>
  <li><strong>dotenv</strong> và <strong>os</strong>: Quản lý biến môi trường.</li>
  <li><strong>openai</strong>: Tương tác với API OpenAI.</li>
  <li><strong>cv2</strong> và <strong>numpy</strong>: Xử lý ảnh.</li>
  <li><strong>ultralytics</strong>: Triển khai YOLO (object detection).</li>
  <li><strong>torch</strong>: Thư viện học sâu.</li>
  <li><strong>pandas</strong> và <strong>matplotlib</strong>: Phân tích và trực quan hóa dữ liệu.</li>
  <li><strong>zipfile</strong>: Làm việc với file nén.</li>
</ul>

<h2>📂 Tài Nguyên Bổ Sung</h2>
<p>Vui lòng tải các file dataset và mô hình từ đường link sau (do kích thước quá lớn và bảo mật API_KEY):</p>
<p>
<a href="https://drive.google.com/drive/folders/1AFkcHa_9TF2WJTkkY7ZwFNmDjO70BirI?usp=sharing" target="_blank">
  👉 Tải dữ liệu và mô hình tại đây 👈
</a>
</p>

<h2>🛠️ Cấu Trúc Source Code</h2>
<pre>
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
</pre>

<h2>🚀 Chạy Chương Trình</h2>
<p>Sau khi cài đặt đầy đủ, chạy lệnh sau để khởi động server:</p>

<pre>
python app.py
</pre>

<p>Mở trình duyệt và truy cập vào: <strong>http://127.0.0.1:5000/</strong></p>

<p><strong>🎉 Chúc bạn thành công!</strong></p>
