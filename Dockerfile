# Базовый образ
FROM python:3.10-slim

# Установка зависимостей
WORKDIR /app
COPY app/ /app/
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду запуска
CMD ["python", "app.py"]
