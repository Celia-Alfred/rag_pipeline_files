from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = FastEmbedEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            batch_size=4
        )

    return embedding_model


def create_embeddings(chunks):
    texts = [chunk["page_content"] for chunk in chunks]

    model = get_embedding_model()
    vectors = model.embed_documents(texts)

    embedded_chunks = []

    for chunk, vector in zip(chunks, vectors):
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page_content": chunk["page_content"],
            "metadata": chunk["metadata"],
            "embedding": vector
        })

    return embedded_chunks