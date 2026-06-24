import streamlit as st

from utils.pdf_loader import extract_text_from_pdf
from utils.chunker import create_chunks
from utils.vector_store import create_vector_store
from utils.rag_chain import generate_answer

# Page Config

st.set_page_config(
    page_title="PDF RAG Chatbot",
    layout="wide"
)

st.title("📄 PDF RAG Chatbot")

# Session State

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents" not in st.session_state:
    st.session_state.documents = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""

# Sidebar

with st.sidebar:

    st.header("⚙️ Controls")

    top_k = st.slider(
        "Retrieved Chunks (Top K)",
        min_value=3,
        max_value=15,
        value=10
    )

    if st.button("🗑️ Reset Chatbot"):

        st.session_state.messages = []
        st.session_state.vector_store = None
        st.session_state.documents = []
        st.session_state.pdf_processed = False
        st.session_state.chunk_count = 0
        st.session_state.pdf_name = ""

        st.rerun()

# Upload PDF

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    st.info(
        f"📄 Selected File: {uploaded_file.name}"
    )

if uploaded_file:

    if st.button("🚀 Process PDF"):

        # Clear previous PDF
        st.session_state.vector_store = None
        st.session_state.documents = []
        st.session_state.messages = []
        st.session_state.pdf_processed = False
        st.session_state.chunk_count = 0
        st.session_state.pdf_name = ""

        import gc
        gc.collect()

        with st.spinner("Processing PDF..."):

            pages = extract_text_from_pdf(
                uploaded_file
            )

            documents = create_chunks(
                pages
            )

            if not documents:

                st.error(
                    "No text could be extracted from the PDF."
                )

                st.stop()

            st.session_state.documents = documents

            vector_store = create_vector_store(
                documents
            )

            st.session_state.vector_store = vector_store
            st.session_state.pdf_processed = True
            st.session_state.chunk_count = len(
                documents
            )
            st.session_state.pdf_name = (
                uploaded_file.name
            )

        st.success(
            "✅ PDF Processed Successfully"
        )

# PDF Statistics

if st.session_state.pdf_processed:

    st.success(
        "✅ PDF Ready for Questions"
    )

    st.subheader(
        "📊 PDF Statistics"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📄 File Name",
            st.session_state.pdf_name
        )

    with col2:

        st.metric(
            "🧩 Chunks Generated",
            st.session_state.chunk_count
        )

# Chat History

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# Chat

if st.session_state.vector_store:

    question = st.chat_input(
        "Ask a question about the PDF..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        # Summary Mode

        summary_keywords = [
            "summary",
            "summarize",
            "summarise",
            "overview",
            "give me summary"
        ]

        is_summary_query = any(
            word in question.lower()
            for word in summary_keywords
        )

        if is_summary_query:

            docs = st.session_state.documents[
                :30
            ]

            results = [
                (doc, 0)
                for doc in docs
            ]

        else:

            results = (
                st.session_state.vector_store
                .similarity_search_with_score(
                    question,
                    k=top_k
                )
            )

            docs = [
                doc
                for doc, score in results
            ]

        # Generate Answer
 
        answer = generate_answer(
            question,
            docs
        )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(answer)

            st.caption(
                f"Retrieved {len(docs)} relevant chunks"
            )

            pages = sorted(
                {
                    doc.metadata.get(
                        "page"
                    )
                    for doc in docs
                    if doc.metadata.get(
                        "page"
                    )
                    is not None
                }
            )

            if pages:

                st.markdown(
                    f"📚 **Sources:** Pages {', '.join(map(str, pages))}"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # Debug

        with st.expander(
            "🔍 Retrieved Chunks & Scores"
        ):

            for i, (
                doc,
                score
            ) in enumerate(results):

                st.markdown(
                    f"### Chunk {i+1}"
                )

                st.write(
                    f"📄 Page: {doc.metadata.get('page')}"
                )

                st.write(
                    f"Similarity Score: {score}"
                )

                st.write(
                    doc.page_content
                )

                st.divider()

else:

    st.info(
        "Upload a PDF and click '🚀 Process PDF' to start chatting."
    )