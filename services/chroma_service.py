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

    if not isinstance(embedded_chunks, list):
        raise ValueError("Expected a list of embedded chunks")

    if len(embedded_chunks) == 0:
        raise ValueError("No embedded chunks provided")

    stored_ids = []

    # Store in small batches to reduce memory usage
    batch_size = 5

    for i in range(0, len(embedded_chunks), batch_size):

        batch = embedded_chunks[i:i + batch_size]

        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in batch:

            if not all(
                key in chunk
                for key in ["chunk_id", "page_content", "metadata", "embedding"]
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

        stored_ids.extend(ids)

    return {
        "count": len(stored_ids),
        "ids": stored_ids
    }