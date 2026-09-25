# rag-data-pipeline
 RAG data pipeline using Flask, MySQL, LangChain, and ChromaDB.
## API Endpoints

| Method | Endpoint |
|---|---|
| GET | `/api/extract` |
| POST | `/api/documents/create` |
| POST | `/api/chunk` |

 
 ## Testing APIs

GET  http://127.0.0.1:5000/api/extract
     → Fetches documents from MySQL.

POST http://127.0.0.1:5000/api/documents/create
     → Creates LangChain Documents from the extracted data.

POST http://127.0.0.1:5000/api/chunk
     → Splits the documents into smaller chunks.


