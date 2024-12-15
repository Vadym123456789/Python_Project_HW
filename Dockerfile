# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install celery redis flask

# Створюємо не root користувача
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Копіюємо файли проекту
COPY . .

# Змінюємо власника файлів
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000