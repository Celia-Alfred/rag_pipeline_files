from flask import Blueprint, jsonify, request

from services.embedd_service import create_embedding
from services.retrieval_service import retrieve_documents
from services.generate_service import generate_answer

retrieval_bp = Blueprint("retrieval", __name__)


@retrieval_bp.route("/api/retrieve", methods=["POST"])
def retrieve_api():
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({
                "status": "error",
                "message": "query is required"
            }), 400

        query = data["query"]
        top_k = data.get("top_k", 3)

        query_embedding = create_embedding(query)

        results = retrieve_documents(query_embedding, top_k)

        retrieved_documents = results["documents"][0]

        answer = generate_answer(query, retrieved_documents)

        return jsonify({
            "status": "success",
            "query": query,
            "answer": answer,
            "sources": results["metadatas"][0]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500