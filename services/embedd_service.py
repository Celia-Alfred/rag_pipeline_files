import os

from huggingface_hub import InferenceClient


MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"


client = InferenceClient(
    token=os.getenv("HF_TOKEN")
)


def create_embedding(text):

    print(
        "EMBED: sending text to Hugging Face API",
        flush=True
    )

    if not text:

        raise ValueError(
            "Text cannot be empty"
        )

    embedding = client.feature_extraction(
        text,
        model=MODEL_NAME
    )

    # Convert numpy array to normal Python list
    if hasattr(embedding, "tolist"):

        embedding = embedding.tolist()

    # Hugging Face can return shape (1, dimensions)
    # for feature extraction.
    if (
        isinstance(embedding, list)
        and len(embedding) == 1
        and isinstance(embedding[0], list)
    ):

        embedding = embedding[0]

    print(
        f"EMBED: embedding created with "
        f"{len(embedding)} dimensions",
        flush=True
    )

    return embedding


def create_embeddings(chunks):

    results = []

    print(
        f"EMBED: creating embeddings for "
        f"{len(chunks)} chunks using Hugging Face API",
        flush=True
    )

    for index, chunk in enumerate(chunks):

        print(
            f"EMBED: processing chunk "
            f"{index + 1}/{len(chunks)}",
            flush=True
        )

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

        embedding = create_embedding(
            chunk["page_content"]
        )

        results.append({
            "chunk_id": chunk["chunk_id"],
            "page_content": chunk["page_content"],
            "metadata": chunk["metadata"],
            "embedding": embedding
        })

    print(
        "EMBED: all embeddings created successfully",
        flush=True
    )

    return results