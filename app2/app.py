import os
from flask import Flask, request, jsonify
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


@app.route("/process_file", methods=["POST"])
def process_file():
    data = request.get_json()
    file_url = data.get("file_url")

    if not file_url:
        return "No file URL provided", 400

    # Здесь можно добавить логику обработки файла
    return f"File at {file_url} successfully received and processed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
