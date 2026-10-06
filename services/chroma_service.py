import chromadb


client = None
collection = None


def get_collection():
    global client, collection

    if collection is None:
        client = chromadb.Client()

        collection = client.get_or_create_collection(
            name="rag_documents_384"
        )

    return collection


def store_embeddings(embedded_chunks):

    if not isinstance(embedded_chunks, list):
        raise ValueError("Expected a list of embedded chunks")

    if len(embedded_chunks) == 0:
        raise ValueError("No embedded chunks provided")

    collection = get_collection()

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for chunk in embedded_chunks:

        if not all(
            key in chunk
            for key in [
                "chunk_id",
                "page_content",
                "metadata",
                "embedding"
            ]
        ):
            raise ValueError(
                "Each chunk must contain chunk_id, page_content, metadata and embedding"
            )

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