from flask import Flask
from flask_cors import CORS

from routes.extract_routes import extract_bp
from routes.document_routes import document_bp
from routes.chunk_routes import chunking_bp
from routes.embedd_routes import embedding_bp
from routes.chroma_routes import chroma_bp

app = Flask(__name__)
CORS(app)

# Register API routes
app.register_blueprint(extract_bp)
app.register_blueprint(document_bp)
app.register_blueprint(chunking_bp)
app.register_blueprint(embedding_bp)
app.register_blueprint(chroma_bp)


@app.route("/")
def home():
    return {
        "message": "RAG Data Pipeline API is running",
        "endpoints": {
            "extract": "GET /api/extract",
            "create_documents": "POST /api/documents/create",
            "chunk": "POST /api/chunk",
            "embed": "POST /api/embed",
            "store": "POST /api/store"
        }
    }


if __name__ == "__main__":
    app.run()