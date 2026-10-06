from flask import Blueprint, jsonify, request

from services.embedd_service import create_embedding
from services.retrieval_service import retrieve_documents
from services.generate_service import generate_answer


retrieval_bp = Blueprint(
    "retrieval",
    __name__
)


@retrieval_bp.route(
    "/api/retrieve",
    methods=["POST"]
)
def retrieve_api():

    print(
        "RETRIEVE API: request received",
        flush=True
    )

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "status": "error",
                "message": "Request body is required"
            }), 400

        if "query" not in data:

            return jsonify({
                "status": "error",
                "message": "query is required"
            }), 400

        query = data["query"]

        if not query or not isinstance(
            query,
            str
        ):

            return jsonify({
                "status": "error",
                "message": "query must be a non-empty string"
            }), 400

        top_k = data.get(
            "top_k",
            3
        )

        if not isinstance(
            top_k,
            int
        ) or top_k <= 0:

            return jsonify({
                "status": "error",
                "message": "top_k must be a positive integer"
            }), 400

        print(
            f"RETRIEVE: query = {query}",
            flush=True
        )

        print(
            "RETRIEVE: creating query embedding",
            flush=True
        )

        query_embedding = create_embedding(
            query
        )

        print(
            "RETRIEVE: query embedding created",
            flush=True
        )

        print(
            f"RETRIEVE: searching top {top_k} documents",
            flush=True
        )

        results = retrieve_documents(
            query_embedding,
            top_k
        )

        retrieved_documents = results[
            "documents"
        ][0]

        print(
            f"RETRIEVE: found "
            f"{len(retrieved_documents)} documents",
            flush=True
        )

        print(
            "RETRIEVE: generating answer",
            flush=True
        )

        answer = generate_answer(
            query,
            retrieved_documents
        )

        print(
            "RETRIEVE: answer generated successfully",
            flush=True
        )

        return jsonify({
            "status": "success",
            "query": query,
            "answer": answer,
            "sources": results[
                "metadatas"
            ][0]
        }), 200

    except Exception as e:

        print(
            f"RETRIEVE API ERROR: {str(e)}",
            flush=True
        )

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500