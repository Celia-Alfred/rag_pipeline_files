import gc

model = None


def get_model():
    global model

    if model is None:

        print("EMBED: loading SentenceTransformer model", flush=True)

        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        print("EMBED: model loaded successfully", flush=True)

    return model


def release_model():

    global model

    print("EMBED: releasing model from memory", flush=True)

    model = None

    gc.collect()

    print("EMBED: model released", flush=True)


def create_embedding(text):

    try:

        model_instance = get_model()

        embedding = model_instance.encode(text)

        return embedding.tolist()

    finally:

        release_model()


def create_embeddings(chunks):

    results = []

    try:

        model_instance = get_model()

        print(
            f"EMBED: creating embeddings for {len(chunks)} chunks",
            flush=True
        )

        for chunk in chunks:

            embedding = model_instance.encode(
                chunk["page_content"]
            )

            results.append({
                "chunk_id": chunk["chunk_id"],
                "page_content": chunk["page_content"],
                "metadata": chunk["metadata"],
                "embedding": embedding.tolist()
            })

        print(
            "EMBED: all embeddings created successfully",
            flush=True
        )

        return results

    finally:

        release_model()