from langchain_core.documents import Document


def create_documents(records):

    documents = []

    for record in records:

        document = Document(
            page_content=record["content"],
            metadata={
                "id": record["id"],
                "title": record["title"],
                "category": record["category"]
            }
        )

        documents.append(document)

    return documents