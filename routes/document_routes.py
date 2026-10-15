
from flask import Blueprint, jsonify, request

from services.document_service import create_documents
from services.chroma_service import delete_document_chunks


document_bp = Blueprint("documents", __name__)


@document_bp.route("/api/documents/create", methods=["POST"])
def create_document_api():
    try:
        records = request.get_json()

        if not records:
            return jsonify({
                "status": "error",
                "message": "No records provided"
            }), 400

        documents = create_documents(records)

        response = []

        for doc in documents:
            response.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            })

        return jsonify({
            "status": "success",
            "count": len(documents),
            "documents": response
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@document_bp.route(
    "/api/documents/<string:document_id>",
    methods=["DELETE"]
)
def delete_document_api(document_id):
    try:
        result = delete_document_chunks(document_id)

        if result["deleted_chunks"] == 0:
            return jsonify({
                "status": "error",
                "message": (
                    "Document not found, or it has already been deleted."
                ),
                "document_id": document_id
            }), 404

        return jsonify({
            "status": "success",
            "message": "Document deleted successfully.",
            "document_id": document_id,
            "deleted_chunks": result["deleted_chunks"]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
