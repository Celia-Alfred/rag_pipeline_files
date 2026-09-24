# rag-data-pipeline
 RAG data pipeline using Flask, MySQL, LangChain, and ChromaDB.
## API Endpoints

| Method | Endpoint |
|---|---|
| GET | `/api/extract` |
| POST | `/api/documents/create` |
| POST | `/api/chunk` |

## Application URL

```text
http://127.0.0.1:5000
 
 ## Testing APIs

API endpoints can be tested using Postman by the following URLs. The output of each stage can be used as input for the next stage.

GET  http://127.0.0.1:5000/api/extract
     → Fetches documents from MySQL.

POST http://127.0.0.1:5000/api/documents/create
     → Creates LangChain Documents from the extracted data.

POST http://127.0.0.1:5000/api/chunk
     → Splits the documents into smaller chunks.


