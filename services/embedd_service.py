import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

client = None


def get_client():
    global client

    if client is None:
        token = os.getenv("HF_TOKEN")

        if not token:
            raise ValueError("HF_TOKEN is not configured")

        client = InferenceClient(
            model=MODEL_ID,
            provider="hf-inference",
            token=token,
            timeout=60
        )

    return client


def create_embedding(text):
    result = get_client().feature_extraction(text)

    embedding = result.tolist() if hasattr(result, "tolist") else result

    if embedding and isinstance(embedding[0], list):
        if len(embedding) == 1:
            embedding = embedding[0]
        else:
            raise ValueError("Unexpected embedding response shape")

    if len(embedding) != 384:
        raise ValueError(
            f"Expected 384 dimensions, received {len(embedding)}"
        )

    return embedding


def create_embeddings(chunks):
    embedded_chunks = []

    for chunk in chunks:
        vector = create_embedding(chunk["page_content"])

        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page_content": chunk["page_content"],
            "metadata": chunk["metadata"],
            "embedding": vector
        })

    return embedded_chunks