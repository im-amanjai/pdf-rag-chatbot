from langchain_chroma import Chroma

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_store(documents):

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store