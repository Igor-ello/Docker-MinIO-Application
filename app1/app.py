import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from minio import Minio
from io import BytesIO
import requests  # Для взаимодействия с app2

app = Flask(__name__)

# Подключение к MinIO
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
    secure=False
)

bucket_name = "mybucket"

# Проверяем наличие бакета и создаем его, если отсутствует
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# URL app2
app2_url = os.getenv("APP2_URL", "http://flask-app2:5001")

@app.route("/")
def index():
    files = minio_client.list_objects(bucket_name)
    file_list = [{'name': obj.object_name} for obj in files]
    return render_template('index.html', files=file_list)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            minio_client.put_object(
                bucket_name, file.filename, file.stream, length=-1, part_size=10*1024*1024
            )
            # Здесь можно добавить запрос к app2, если нужно
            return redirect(url_for("index"))
    return render_template("upload.html")

@app.route("/download/<filename>")
def download_file(filename):
    response = minio_client.get_object(bucket_name, filename)
    return send_file(BytesIO(response.read()), as_attachment=True, download_name=filename)

@app.route("/delete/<filename>")
def delete_file(filename):
    minio_client.remove_object(bucket_name, filename)
    return redirect(url_for("index"))

@app.route("/send_to_app2/<filename>")
def send_to_app2(filename):
    # Формируем URL файла в MinIO
    file_url = f"http://{os.getenv('MINIO_ENDPOINT', 'minio:9000')}/{bucket_name}/{filename}"

    # Передаем запрос к app2
    response = requests.post(
        f"{app2_url}/process_file",
        json={"file_url": file_url}  # Передаем URL файла
    )

    if response.status_code == 200:
        return f"File {filename} successfully processed by app2: {response.text}"
    else:
        return f"Failed to process file {filename}. Error: {response.status_code} - {response.text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
