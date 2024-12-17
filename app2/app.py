import os
from flask import Flask, request, jsonify, render_template
from minio import Minio

app = Flask(__name__)

# Подключение к MinIO
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
    secure=False
)

bucket_name = "mybucket"
processed_files = []  # Список для хранения информации о обработанных файлах

@app.route("/process_file", methods=["POST"])
def process_file():
    data = request.get_json()
    file_url = data.get("file_url")

    if not file_url:
        return "No file URL provided", 400

    # Логика обработки файла (можно добавить больше шагов обработки)
    processed_files.append(file_url)

    # Добавляем информацию о файле в список обработанных
    return jsonify({
        "message": f"File at {file_url} successfully received and processed",
        "file_url": file_url
    })


@app.route("/")
def index():
    # Отображаем список обработанных файлов на главной странице
    return render_template("index.html", processed_files=processed_files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
