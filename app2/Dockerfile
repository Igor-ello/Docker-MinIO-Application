FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask minio
CMD ["python", "app.py"]
