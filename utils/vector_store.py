from langchain_chroma import Chroma
from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)
from chromadb.config import Settings
import tempfile

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(documents):

    persist_dir = tempfile.mkdtemp()

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
        client_settings=Settings(
            anonymized_telemetry=False
        )
    )

    return vector_store