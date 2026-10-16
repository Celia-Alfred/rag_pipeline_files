<<<<<<< HEAD
## Deployed API

[Render] https://rag-data-pipeline.onrender.com

## API Endpoints

| Method | Endpoint |
|---|---|
| GET | `/api/extract` |
| POST | `/api/documents/create` |
| POST | `/api/chunk` |
| POST | `/api/embed` | Generate embeddings |
| POST | `/api/store` | Store embeddings in ChromaDB |
 
=======
# RAG Document Processing API

A Flask-based RAG API that supports PDF and TXT document uploads, text extraction, chunking, embedding generation, vector storage, and AI-powered question answering.

**Deployed URL:** https://rag-pipeline-files.onrender.com

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|

| POST | `/api/chat` | Ask questions about uploaded documents |

| DELETE | `/api/documents/<document_id>` | Delete a document |

>>>>>>> generation


