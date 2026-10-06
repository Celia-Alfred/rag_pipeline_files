from flask import Blueprint, jsonify, request

from services.chroma_service import store_embeddings


chroma_bp = Blueprint(
    "chroma",
    __name__
)


@chroma_bp.route(
    "/api/store",
    methods=["POST"]
)
def store_api():

    print(
        "STORE API: request received",
        flush=True
    )

    try:

        embedded_chunks = request.get_json()

        print(
            f"STORE API: received data type: "
            f"{type(embedded_chunks)}",
            flush=True
        )

        if not embedded_chunks:

            return jsonify({
                "status": "error",
                "message": "No embeddings provided"
            }), 400

        if not isinstance(
            embedded_chunks,
            list
        ):

            return jsonify({
                "status": "error",
                "message": (
                    "Request body must be a list "
                    "of embedded chunks"
                )
            }), 400

        result = store_embeddings(
            embedded_chunks
        )

        return jsonify({
            "status": "success",
            "message": (
                "Embeddings stored successfully "
                "in ChromaDB"
            ),
            "count": result["count"],
            "ids": result["ids"]
        }), 200

    except Exception as e:

        print(
            f"STORE API ERROR: {str(e)}",
            flush=True
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500