import hashlib
import math

EMBEDDING_DIMENSION = 384


def create_embedding(text):
    vector = [0.0] * EMBEDDING_DIMENSION

    words = text.lower().split()

    for word in words:
        digest = hashlib.sha256(word.encode("utf-8")).digest()

        for i in range(0, len(digest), 2):
            value = int.from_bytes(digest[i:i + 2], "big")
            index = value % EMBEDDING_DIMENSION

            sign = 1.0 if value % 2 == 0 else -1.0
            vector[index] += sign

    magnitude = math.sqrt(sum(x * x for x in vector))

    if magnitude > 0:
        vector = [x / magnitude for x in vector]

    return vector


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