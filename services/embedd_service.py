from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_embeddings(chunks):
    texts = [chunk["page_content"] for chunk in chunks]

    vectors = embedding_model.embed_documents(texts)

    embedded_chunks = []

    for chunk, vector in zip(chunks, vectors):
        embedded_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "page_content": chunk["page_content"],
            "metadata": chunk["metadata"],
            "embedding": vector
        })

    return embedded_chunks