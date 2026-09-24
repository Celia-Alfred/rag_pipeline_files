from flask import Flask
from flask_cors import CORS

from routes.extract_routes import extract_bp
from routes.document_routes import document_bp
from routes.chunk_routes import chunking_bp


app = Flask(__name__)

CORS(app)

app.register_blueprint(extract_bp)
app.register_blueprint(document_bp)
app.register_blueprint(chunking_bp)


@app.route("/")
def home():
    return {
        "message": "RAG Data Pipeline API is running"
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)