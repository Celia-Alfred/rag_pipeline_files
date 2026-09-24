from flask import Blueprint, jsonify, request

from services.document_service import create_documents


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
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500