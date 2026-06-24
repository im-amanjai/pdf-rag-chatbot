from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def create_chunks(pages):

    documents = []

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        text_length = len(text)

        # Small documents (resume, notes)
        if text_length < 10000:

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100
            )

        # Medium documents
        elif text_length < 100000:

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=150
            )

        # Large books/docs
        else:

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=200
            )

        chunks = splitter.split_text(text)

        for chunk in chunks:

            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "page": page_number
                    }
                )
            )

    return documents