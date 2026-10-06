from flask import Blueprint, jsonify, request

from services.embedd_service import create_embeddings


embedding_bp = Blueprint(
    "embedding",
    __name__
)


@embedding_bp.route(
    "/api/embed",
    methods=["POST"]
)
def embed_api():

    print(
        "EMBED API: request received",
        flush=True
    )

    try:

        chunks = request.get_json()

        print(
            f"EMBED API: received data type: "
            f"{type(chunks)}",
            flush=True
        )

        if not chunks:

            return jsonify({
                "status": "error",
                "message": "No chunks provided"
            }), 400

        if not isinstance(chunks, list):

            return jsonify({
                "status": "error",
                "message": (
                    "Request body must be a list "
                    "of chunks"
                )
            }), 400

        embedded_chunks = create_embeddings(
            chunks
        )

        return jsonify(
            embedded_chunks
        ), 200

    except Exception as e:

        print(
            f"EMBED API ERROR: {str(e)}",
            flush=True
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500