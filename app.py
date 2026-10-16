import json
from flask import Flask, Response
from flask_cors import CORS
from routes.extract_routes import extract_bp
from routes.document_routes import document_bp
from routes.chunk_routes import chunking_bp
from routes.embedd_routes import embedding_bp
from routes.chroma_routes import chroma_bp
from routes.retrieval_routes import retrieval_bp
from routes.chat_routes import chat_bp
app = Flask(__name__)
CORS(app)

app.register_blueprint(extract_bp)
app.register_blueprint(document_bp)
app.register_blueprint(chunking_bp)
app.register_blueprint(embedding_bp)
app.register_blueprint(chroma_bp)
app.register_blueprint(retrieval_bp)
app.register_blueprint(chat_bp)

@app.route("/")
def home():
    response = {
        "message": "RAG Document Processing API is running",
        "endpoints": {
            "upload and retrieve": "POST /api/chat",
            "Delete": "DELETE /api/documents/<document_id>"
        },
        "supported_formats": ["PDF", "TXT"]
    }   
    return Response(
        json.dumps(response, indent=2),
        mimetype="application/json"
    )
if __name__ == "__main__":
    app.run()