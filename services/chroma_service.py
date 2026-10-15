
client = None
collection = None


def get_collection():
    global client, collection

    print("STORE: get_collection started", flush=True)

    if collection is None:
        try:
            import chromadb
            print("CHROMA: import successful", flush=True)
        except Exception as e:
            print(f"CHROMA IMPORT ERROR: {str(e)}", flush=True)
            raise

        print("STORE: creating PersistentClient", flush=True)

        client = chromadb.PersistentClient(path="./chroma_db")

        print("STORE: PersistentClient created", flush=True)

        collection = client.get_or_create_collection(
            name="rag_documents_jina"
        )

        print(
            f"CHROMA: using collection '{collection.name}'",
            flush=True
        )

    return collection


def store_embeddings(embedded_chunks):
    print("STORE: store_embeddings started", flush=True)

    if not isinstance(embedded_chunks, list):
        raise ValueError("Embedded chunks must be provided as a list.")

    if not embedded_chunks:
        raise ValueError("No embedded chunks provided.")

    print(f"STORE: received {len(embedded_chunks)} chunks", flush=True)

    collection = get_collection()
    stored_ids = []
    batch_size = 5

    for start in range(0, len(embedded_chunks), batch_size):
        batch = embedded_chunks[start:start + batch_size]

        print(f"STORE: processing batch starting at {start}", flush=True)

        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in batch:
            for key in ("chunk_id", "page_content", "metadata", "embedding"):
                if key not in chunk:
                    raise ValueError(f"Missing {key} in embedded chunk.")

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

        print(f"STORE: batch {start} stored successfully", flush=True)
        stored_ids.extend(ids)

    print("STORE: all embeddings stored successfully", flush=True)

    return {
        "count": len(stored_ids),
        "ids": stored_ids
    }


def retrieve_embeddings(query_embedding, top_k=3):
    print("RETRIEVE: getting collection", flush=True)

    collection = get_collection()
    total_chunks = collection.count()

    if total_chunks == 0:
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

    top_k = max(1, min(top_k, total_chunks))

    print(f"RETRIEVE: searching top {top_k} chunks", flush=True)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    print("RETRIEVE: search completed", flush=True)

    return results


def delete_document_chunks(document_id):
    """Delete all ChromaDB chunks belonging to one document."""

    if not isinstance(document_id, str) or not document_id.strip():
        raise ValueError("A valid document_id is required.")

    document_id = document_id.strip()

    print(
        f"DELETE: searching chunks for document {document_id}",
        flush=True
    )

    collection = get_collection()

    results = collection.get(
        where={"document_id": document_id},
        include=["metadatas"]
    )

    chunk_ids = results.get("ids", [])

    if not chunk_ids:
        print(
            f"DELETE: no chunks found for document {document_id}",
            flush=True
        )

        return {
            "document_id": document_id,
            "deleted_chunks": 0
        }

    collection.delete(ids=chunk_ids)

    print(
        f"DELETE: successfully removed {len(chunk_ids)} chunks",
        flush=True
    )

    return {
        "document_id": document_id,
        "deleted_chunks": len(chunk_ids)
    }
