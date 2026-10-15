
from services.chroma_service import get_collection


def retrieve_documents(query_embedding, top_k=20, max_distance=None):
    """Retrieve relevant document chunks from ChromaDB."""

    print("RETRIEVE SERVICE: getting Chroma collection", flush=True)

    collection = get_collection()
    total_chunks = collection.count()

    if total_chunks == 0:
        print("No documents found in ChromaDB.", flush=True)
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "ids": [[]]
        }

    top_k = max(1, min(int(top_k), total_chunks))

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    documents = results.get("documents", [[]])[0] or []
    metadatas = results.get("metadatas", [[]])[0] or []
    distances = results.get("distances", [[]])[0] or []
    ids = results.get("ids", [[]])[0] or []

    candidates = []

    for i, document in enumerate(documents):
        metadata = metadatas[i] if i < len(metadatas) else {}
        distance = distances[i] if i < len(distances) else None
        chunk_id = ids[i] if i < len(ids) else None

        candidates.append({
            "document": document,
            "metadata": metadata or {},
            "distance": distance,
            "id": chunk_id
        })

    if max_distance is not None:
        candidates = [
            item for item in candidates
            if item["distance"] is not None
            and item["distance"] <= max_distance
        ]

    print("\n RETRIEVED CHUNKS ", flush=True)

    for i, item in enumerate(candidates, start=1):
        print(f"\nChunk {i}", flush=True)
        print(f"ID: {item['id']}", flush=True)
        print(f"Source: {item['metadata'].get('source')}", flush=True)
        print(f"Page: {item['metadata'].get('page')}", flush=True)
        print(f"Distance: {item['distance']}", flush=True)
        print(f"Text: {item['document']}", flush=True)

    print(f"\nRelevant candidates returned: {len(candidates)}",
          flush=True)
    print("END RETRIEVED CHUNKS \n", flush=True)

    return {
        **results,
        "documents": [[item["document"] for item in candidates]],
        "metadatas": [[item["metadata"] for item in candidates]],
        "distances": [[item["distance"] for item in candidates]],
        "ids": [[item["id"] for item in candidates]]
    }
