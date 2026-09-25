from flask import Blueprint, jsonify, request
from services.embedd_service import create_embeddings
embedding_bp = Blueprint("embedding", __name__)
@embedding_bp.route("/api/embed", methods=["POST"])
def embed_api():
    try:
        chunks = request.get_json()

        if not chunks:
            return jsonify({
                "status": "error",
                "message": "No chunks provided"
            }), 400

        embedded_chunks = create_embeddings(chunks)

        return jsonify({
            "status": "success",
            "count": len(embedded_chunks),
            "embeddings": embedded_chunks
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500