FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FASTEMBED_CACHE_PATH=/app/fastembed_cache

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

RUN python -c "from fastembed import TextEmbedding; m=TextEmbedding(model_name='sentence-transformers/all-MiniLM-L6-v2', cache_dir='/app/fastembed_cache', threads=1); list(m.embed(['warmup']))"

COPY . .

CMD ["sh", "-c", "exec gunicorn --workers 1 --timeout 300 --bind 0.0.0.0:${PORT:-8000} app:app"]