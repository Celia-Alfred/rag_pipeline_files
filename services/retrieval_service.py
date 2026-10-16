
import re
from pathlib import Path

from services.chroma_service import get_collection


IGNORED_FILENAME_WORDS = {
    "resume","pdf", "txt", "doc", "document", "file"
}

IGNORED_QUESTION_WORDS = {
    "what", "which", "who", "when", "where", "why","how"     
}

def get_filename_tokens(filename):
    filename = Path(filename).stem.lower()
    tokens = set(re.findall(r"[a-z]+", filename))
    return tokens - IGNORED_FILENAME_WORDS


def find_requested_source(question):
    """
    Identify a uniquely mentioned uploaded document.
    Returns the exact source filename or None.
    """

    collection = get_collection()

    stored = collection.get(include=["metadatas"])
    metadatas = stored.get("metadatas", []) or []

    available_sources = sorted({
        metadata.get("source")
        for metadata in metadatas
        if metadata and metadata.get("source")
    })

    question_tokens = set(
        re.findall(r"[a-z]+", question.lower())
    ) - IGNORED_QUESTION_WORDS

    matches = []

    for source in available_sources:
        filename_tokens = get_filename_tokens(source)

        if filename_tokens.intersection(question_tokens):
            matches.append(source)

    if len(matches) == 1:
        print(
            f"Requested document: {matches[0]}",
            flush=True
        )
        return matches[0]

    if len(matches) > 1:
        print(
            f"Multiple documents matched the question: {matches}",
            flush=True
        )

    return None

def retrieve_documents(
    query_embedding,
    top_k=20,
    max_distance=None,
    source_filter=None
):
    """Retrieve relevant chunks, optionally from one document."""

    print(
        "RETRIEVE SERVICE: getting Chroma collection",
        flush=True
    )

    collection = get_collection()

    where = {"source": source_filter} if source_filter else None

    if where:
        matching_chunks = collection.get(
            where=where,
            include=[]
        )
        total_chunks = len(
            matching_chunks.get("ids", [])
        )
    else:
        total_chunks = collection.count()

    if total_chunks == 0:
        print(
            "No matching documents found in ChromaDB.",
            flush=True
        )
        return {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "ids": [[]]
        }

    top_k = max(1, min(int(top_k), total_chunks))

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    if where:
        query_args["where"] = where

    results = collection.query(**query_args)

    documents = results.get("documents", [[]])[0] or []
    metadatas = results.get("metadatas", [[]])[0] or []
    distances = results.get("distances", [[]])[0] or []
    ids = results.get("ids", [[]])[0] or []

    candidates = []

    for i, document in enumerate(documents):
        metadata = (
            metadatas[i]
            if i < len(metadatas)
            else {}
        )

        distance = (
            distances[i]
            if i < len(distances)
            else None
        )

        chunk_id = ids[i] if i < len(ids) else None

        candidates.append({
            "document": document,
            "metadata": metadata or {},
            "distance": distance,
            "id": chunk_id
        })

    if max_distance is not None:
        candidates = [
            item
            for item in candidates
            if item["distance"] is not None
            and item["distance"] <= max_distance
        ]

    print("\nRETRIEVED CHUNKS", flush=True)

    for i, item in enumerate(candidates, start=1):
        print(f"\nChunk {i}", flush=True)
        print(f"ID: {item['id']}", flush=True)
        print(
            f"Source: {item['metadata'].get('source')}",
            flush=True
        )
        print(
            f"Page: {item['metadata'].get('page')}",
            flush=True
        )
        print(f"Distance: {item['distance']}", flush=True)

    print(
        f"\nRelevant candidates returned: {len(candidates)}",
        flush=True
    )
    print("END RETRIEVED CHUNKS\n", flush=True)

    return {
        **results,
        "documents": [
            [item["document"] for item in candidates]
        ],
        "metadatas": [
            [item["metadata"] for item in candidates]
        ],
        "distances": [
            [item["distance"] for item in candidates]
        ],
        "ids": [
            [item["id"] for item in candidates]
        ]
    }
