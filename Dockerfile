FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .

CMD ["sh", "-c", "exec gunicorn --workers 1 --timeout 300 --bind 0.0.0.0:${PORT:-8000} app:app"]