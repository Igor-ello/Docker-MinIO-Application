import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from minio import Minio
from io import BytesIO

app = Flask(__name__)

# Подключение к MinIO через переменные среды
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


@app.route("/")
@app.route('/')
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
