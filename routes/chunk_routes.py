from flask import Blueprint, jsonify, request

from services.chunk_service import chunk_documents
from langchain_core.documents import Document

chunking_bp = Blueprint("chunking", __name__)

@chunking_bp.route("/api/chunk", methods=["POST"])
def chunk_api():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No documents provided"
            }), 400

        documents = []

        for item in data:

            document = Document(
                page_content=item["page_content"],
                metadata=item["metadata"]
            )

            documents.append(document)

        chunks = chunk_documents(documents)

        response = []

        for index, chunk in enumerate(chunks):

            response.append({
                "chunk_id": index,
                "page_content": chunk.page_content,
                "metadata": chunk.metadata
            })

        return jsonify({
            "status": "success",
            "count": len(chunks),
            "chunks": response
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500