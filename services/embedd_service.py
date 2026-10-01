from sentence_transformers import SentenceTransformer

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    return model


def create_embedding(text):
    model = get_model()

    embedding = model.encode(text)

    return embedding.tolist()


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