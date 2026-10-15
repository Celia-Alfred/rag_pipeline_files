
from uuid import uuid4
from pathlib import Path

from flask import Blueprint, request, jsonify
from langchain_core.documents import Document

from services.file_service import extract_file_content
from services.chunk_service import chunk_documents
from services.embedd_service import create_embeddings, create_embedding
from services.chroma_service import store_embeddings
from services.retrieval_service import retrieve_documents
from services.generate_service import generate_answer


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():

    if request.files.getlist("files"):
        files = request.files.getlist("files")
        uploaded_files = []
        errors = []

        for file in files:
            if not file.filename:
                continue

            filename = Path(file.filename).name
            document_id = str(uuid4())

            try:
                pages = extract_file_content(file)

                documents = [
                    Document(
                        page_content=page["content"],
                        metadata={
                            "document_id": document_id,
                            "source": filename,
                            "page": page["page"]
                        }
                    )
                    for page in pages
                ]

                chunks = chunk_documents(documents)

                if not chunks:
                    raise ValueError(
                        "No text chunks could be created."
                    )

                chunk_data = [
                    {
                        "chunk_id": str(uuid4()),
                        "page_content": chunk.page_content,
                        "metadata": {
                            **chunk.metadata,
                            "document_id": document_id,
                            "source": filename
                        }
                    }
                    for chunk in chunks
                ]

                embedded_chunks = create_embeddings(chunk_data)

                result = store_embeddings(embedded_chunks)

                uploaded_files.append({
                    "document_id": document_id,
                    "filename": filename,
                    "chunks_stored": result["count"]
                })

            except Exception as error:
                import traceback
                traceback.print_exc()

                errors.append({
                    "filename": filename,
                    "message": str(error)
                })

        if uploaded_files and not errors:
            return jsonify({
                "status": "success",
                "message": (
                    "Your document is ready! "
                    "You can ask your questions now."
                ),
                "uploaded_files": uploaded_files
            }), 200

        if uploaded_files:
            return jsonify({
                "status": "partial_success",
                "message": (
                    "Some files were processed successfully."
                ),
                "uploaded_files": uploaded_files,
                "errors": errors
            }), 200

        return jsonify({
            "status": "error",
            "message": "No files could be processed.",
            "errors": errors or [
                {
                    "message": (
                        "Please upload a PDF or TXT file."
                    )
                }
            ]
        }), 400

    data = request.get_json(silent=True) or {}
    question = data.get("question")

    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "status": "error",
            "message": (
                "Please upload a file using form-data key 'files', "
                "or send a question using JSON key 'question'."
            )
        }), 400

    try:
        question = question.strip()

        query_embedding = create_embedding(question)

        results = retrieve_documents(
            query_embedding,
            top_k=20
        )

        retrieved_documents = results.get(
            "documents", [[]]
        )[0]

        source_metadata = results.get(
            "metadatas", [[]]
        )[0]

        if not retrieved_documents:
            return jsonify({
                "status": "error",
                "message": (
                    "No document content found. "
                    "Please upload a document first."
                )
            }), 404

        question_words = {
            word.lower().strip(".,?!:;()[]{}\"'")
            for word in question.split()
            if len(word.strip(".,?!:;()[]{}\"'")) > 2
        }

        relevant_documents = []
        relevant_sources = []
        seen = set()

        for index, document in enumerate(retrieved_documents):

            source = (
                source_metadata[index]
                if index < len(source_metadata)
                else {}
            )

            document_text = document.lower()

            if not any(
                word in document_text
                for word in question_words
            ):
                continue

            key = (
                source.get("document_id"),
                source.get("page"),
                source.get("source")
            )

            if key in seen:
                continue

            seen.add(key)
            relevant_documents.append(document)
            relevant_sources.append(source)

        if not relevant_documents:
            return jsonify({
                "status": "error",
                "message": (
                    "No sufficiently relevant source pages "
                    "were found for this question. "
                    "Try rephrasing your question."
                )
            }), 404

        answer = generate_answer(
            question,
            relevant_documents
        )

        return jsonify({
            "status": "success",
            "answer": answer,
            "sources": relevant_sources
        }), 200

    except Exception as error:
        import traceback
        traceback.print_exc()

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500
