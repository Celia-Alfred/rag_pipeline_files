from services.chroma_service import get_collection


def retrieve_documents(
    query_embedding,
    top_k=3
):

    print(
        "RETRIEVE SERVICE: getting Chroma collection",
        flush=True
    )

    collection = get_collection()

    print(
        f"RETRIEVE SERVICE: searching top "
        f"{top_k} documents",
        flush=True
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    print(
        "RETRIEVE SERVICE: search completed",
        flush=True
    )

    return results