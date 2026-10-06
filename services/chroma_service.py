client = None
collection = None


def get_collection():
    global client, collection

    print("STORE: get_collection started", flush=True)

    if collection is None:

        print("STORE: importing chromadb", flush=True)

        import chromadb

        print("STORE: creating PersistentClient", flush=True)

        client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        print("STORE: PersistentClient created", flush=True)

        collection = client.get_or_create_collection(
            name="rag_documents"
        )

        print("STORE: collection created", flush=True)

    return collection


def store_embeddings(embedded_chunks):

    print("STORE: store_embeddings started", flush=True)

    if not isinstance(embedded_chunks, list):
        raise ValueError(
            "Request body must be a list of embedded chunks"
        )

    if len(embedded_chunks) == 0:
        raise ValueError(
            "No embedded chunks provided"
        )

    print(
        f"STORE: received {len(embedded_chunks)} chunks",
        flush=True
    )

    collection = get_collection()

    stored_ids = []

    batch_size = 5

    for start in range(0, len(embedded_chunks), batch_size):

        batch = embedded_chunks[
            start:start + batch_size
        ]

        print(
            f"STORE: processing batch starting at {start}",
            flush=True
        )

        ids = []
        documents = []
        metadatas = []
        embeddings = []

        for chunk in batch:

            if "chunk_id" not in chunk:
                raise ValueError(
                    "Missing chunk_id"
                )

            if "page_content" not in chunk:
                raise ValueError(
                    "Missing page_content"
                )

            if "metadata" not in chunk:
                raise ValueError(
                    "Missing metadata"
                )

            if "embedding" not in chunk:
                raise ValueError(
                    "Missing embedding"
                )

            ids.append(
                str(chunk["chunk_id"])
            )

            documents.append(
                chunk["page_content"]
            )

            metadatas.append(
                chunk["metadata"]
            )

            embeddings.append(
                chunk["embedding"]
            )

        print(
            f"STORE: upserting {len(ids)} chunks",
            flush=True
        )

        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

        print(
            f"STORE: batch {start} stored successfully",
            flush=True
        )

        stored_ids.extend(ids)

    print(
        "STORE: all embeddings stored successfully",
        flush=True
    )

    return {
        "count": len(stored_ids),
        "ids": stored_ids
    }


def retrieve_embeddings(query_embedding, top_k=3):

    print("RETRIEVE: getting collection", flush=True)

    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results