from fastembed import TextEmbedding

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = TextEmbedding(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_dir="/app/fastembed_cache",
            threads=1
        )

    return embedding_model


def create_embeddings(chunks):
    model = get_embedding_model()

    texts = [chunk["page_content"] for chunk in chunks]

    vectors = list(
        model.embed(
            texts,
            batch_size=1
        )
    )

    embedded_chunks = []

    for chunk, vector in zip(chunks, vectors):
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page_content": chunk["page_content"],
            "metadata": chunk["metadata"],
            "embedding": vector.tolist()
        })

    return embedded_chunks