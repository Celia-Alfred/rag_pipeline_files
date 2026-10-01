client = None
collection = None


def get_collection():
    global client, collection

    if collection is None:
        import chromadb

        client = chromadb.PersistentClient(path="./chroma_db")

        collection = client.get_or_create_collection(
            name="rag_documents"
        )

    return collection


def store_embeddings(embedded_chunks):
    collection = get_collection()

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in embedded_chunks:
        ids.append(str(chunk["chunk_id"]))
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


def retrieve_embeddings(query_embedding, top_k=3):
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results