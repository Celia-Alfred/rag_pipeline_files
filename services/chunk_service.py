from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=30
    )
    chunks = splitter.split_documents(documents)

    return chunks