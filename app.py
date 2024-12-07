import os
import base64
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv 
import openai
from openai import OpenAI
import cv2
import matplotlib.pyplot as plt
import os
from ultralytics import YOLO

load_dotenv()

app = Flask(__name__)
openai_api_key = os.getenv("OPENAI_API_KEY")
model_path = os.path.join(os.path.dirname(__file__), "best_model_yolov8m.pt")
model = YOLO(model_path)

def initialize_openai_client():
    return openai.OpenAI(api_key=openai_api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

@app.route("/", methods=["GET"])
def page():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def postImage():
    UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    PROCESSED_PATH = os.path.join(os.path.dirname(__file__), 'static', 'processed')
    unique_classes_detected = set()


    for path in [UPLOAD_PATH, PROCESSED_PATH]:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print(f"Created directory: {path}")
            except OSError as e:
                print(f"Error creating directory: {e}")
                raise

    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            error_message = "No file was uploaded. Please try again."
            return render_template("index.html", error_message=error_message)

        uploaded_file = request.files["file"]
        file_path = os.path.join(UPLOAD_PATH, uploaded_file.filename)
        uploaded_file.save(file_path)

        file_type = uploaded_file.content_type

        if file_type.startswith("image/"):
            img = cv2.imread(file_path)
            results = model.predict(source=file_path, save=True, conf=0.7)
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = box.conf[0]
                    class_id = box.cls[0]
                    class_name = model.names[int(class_id)]
                    unique_classes_detected.add(class_name)

                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    label = f"{class_name} {conf:.2f}"
                    (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 2)
                    cv2.rectangle(
                        img,
                        (int(x1), int(y1) - label_height - baseline - 5),
                        (int(x1) + label_width, int(y1)),
                        (0, 0, 255),
                        -1,
                    )

                    cv2.putText(
                        img,
                        label,
                        (int(x1), int(y1) - baseline - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        (255, 255, 255),
                        2,
                    )

            processed_path = os.path.join(PROCESSED_PATH, f"processed_{uploaded_file.filename}")
            cv2.imwrite(processed_path, img)
            with open(processed_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            data = {
                "processed_image": base64_image,
                "list_traffic_sign_detech": list(unique_classes_detected),
            }

        elif file_type.startswith("video/"):
            cap = cv2.VideoCapture(file_path)
            fourcc = cv2.VideoWriter_fourcc(*'H264')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            processed_video_path = os.path.join(PROCESSED_PATH, f"processed_{uploaded_file.filename}")
            out = cv2.VideoWriter(processed_video_path, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = model.predict(source=frame, save=False, conf=0.7)
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        conf = box.conf[0]
                        class_id = box.cls[0]
                        class_name = model.names[int(class_id)]
                        unique_classes_detected.add(class_name)

                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)

                        font_scale = 2
                        text_thickness = 3 

                        label = f"{class_name} {conf:.2f}"

                        (label_width, label_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)

                        cv2.rectangle(
                            frame,
                            (int(x1), int(y1) - label_height - baseline - 5), 
                            (int(x1) + label_width, int(y1)),
                            (0, 0, 255),
                            -1,  
                        )

                       
                        cv2.putText(
                            frame,
                            label,
                            (int(x1), int(y1) - baseline - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale,  
                            (255, 255, 255),  
                            text_thickness,  
                        )
                out.write(frame)

            cap.release()
            out.release()

            video_url = f"../static/processed/processed_{uploaded_file.filename}"

            data = {
                "processed_video": video_url,
                "list_traffic_sign_detech": list(unique_classes_detected),
            }

        else:
            error_message = "Unsupported file type. Please upload an image or video."
            return render_template("index.html", error_message=error_message)

        return render_template("index.html", dataResponse=data)
    

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.get_json() 
    sign = data.get('sign')
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=300,
            messages=[
            {
                "role": "user",
                "content": (
                    "Hãy giải thích ý nghĩa của biển báo giao thông này. Đây là biển báo của Việt Nam nha giải thích theo ý nghĩa của Việt Nam"
                    f"Nội dung biển báo: {sign}"
                    "Đồng thời, hãy đưa ra các ví dụ minh họa và mức phạt nếu vi phạm. "
                    "Hãy trả về thông tin theo đúng định dạng sau (mỗi mục bắt đầu trên một dòng mới):\n\n"
                    "Ý nghĩa:\n"
                    "- ...\n"
                    "- ...\n\n"
                    "Ví dụ:\n"
                    "- ...\n"
                    "- ...\n\n"
                    "Mức phạt:\n"
                    "- ...\n"
                    "- ...\n\n"
                )
            }
        ],
            temperature=0.7
        )
        response = chat_completion.choices[0].message.content
        print(response)
        return jsonify({"response": response})
    except Exception as e:
        print(f"An error occured: {e}")


@app.route("/clear", methods=["DELETE"])
def clearImage():
    UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    PROCESSED_PATH = os.path.join(os.path.dirname(__file__), 'static', 'processed')

    for path in [UPLOAD_PATH, PROCESSED_PATH]:
        if os.path.exists(path):
            try:
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting files in {path}: {e}")
        else:
            print(f"Directory does not exist: {path}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)



