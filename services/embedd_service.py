
import os
import requests


JINA_API_URL = "https://api.jina.ai/v1/embeddings"
MODEL_NAME = "jina-embeddings-v2-base-en"


def create_embedding(text):
    api_key = os.getenv("JINA_API_KEY")

    if not api_key:
        raise ValueError("JINA_API_KEY is missing from environment variables.")

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    response = requests.post(
        JINA_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL_NAME,
            "input": [text],
            "embedding_type": "float",
            "normalized": True
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()
    return data["data"][0]["embedding"]


def create_embeddings(chunks):
    results = []

    if not chunks:
        raise ValueError("No chunks provided.")

    texts = []

    for chunk in chunks:
        for key in ("chunk_id", "page_content", "metadata"):
            if key not in chunk:
                raise ValueError(f"Missing {key}.")

        texts.append(chunk["page_content"])

    api_key = os.getenv("JINA_API_KEY")

    if not api_key:
        raise ValueError("JINA_API_KEY is missing from environment variables.")

    batch_size = 32

    for start in range(0, len(chunks), batch_size):
        batch_chunks = chunks[start:start + batch_size]
        batch_texts = texts[start:start + batch_size]

        response = requests.post(
            JINA_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "input": batch_texts,
                "embedding_type": "float",
                "normalized": True
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()["data"]

        for item in data:
            chunk = batch_chunks[item["index"]]

            results.append({
                "chunk_id": chunk["chunk_id"],
                "page_content": chunk["page_content"],
                "metadata": chunk["metadata"],
                "embedding": item["embedding"]
            })

    return results
