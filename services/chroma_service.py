import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="rag_documents"
)


def store_embeddings(embedded_chunks):
    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in embedded_chunks:
        chunk_id = str(chunk["chunk_id"])

        ids.append(chunk_id)
        documents.append(chunk["page_content"])
        metadatas.append(chunk["metadata"])
        embeddings.append(chunk["embedding"])

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    return {
        "count": len(ids),
        "ids": ids
    }