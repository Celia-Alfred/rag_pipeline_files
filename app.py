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
    return """
    <html>
        <head>
            <title>RAG Data Pipeline API</title>
        </head>
        <body>
            <h1>RAG Data Pipeline API is running</h1>

            <h2>Available API Endpoints</h2>

            <p><b>GET</b> /api/extract</p>
            <p><b>POST</b> /api/documents/create</p>
            <p><b>POST</b> /api/chunk</p>
            <p><b>POST</b> /api/embed</p>
            <p><b>POST</b> /api/store</p>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run()