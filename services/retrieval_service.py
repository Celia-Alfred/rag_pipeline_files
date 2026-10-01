from services.chroma_service import get_collection


def retrieve_documents(query_embedding, top_k=3):
    collection = get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results