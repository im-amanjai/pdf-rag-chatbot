# 📄 PDF RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to upload PDF documents, generate intelligent summaries, and ask questions directly from the uploaded PDF using AI.

Built using **Streamlit, LangChain, ChromaDB, Sentence Transformers, and Google Gemini/Ollama**.

---

## 🚀 Live Demo

Add your deployed Streamlit link here:

```text
https://pdf-rag-chatbot-rag.streamlit.app/
```

---

## 📌 Project Overview

Reading large PDFs can be time-consuming. This project solves that problem by allowing users to:

* Upload any PDF document
* Automatically process and understand the document
* Generate document summaries
* Ask questions in natural language
* Get answers only from the uploaded PDF
* View source page references used to generate answers

This ensures accurate and context-aware responses without manually searching through the document.

---

## ✨ Features

### 📄 PDF Upload

Upload any PDF document directly from the browser.

### ✂️ Intelligent Text Chunking

Large PDFs are automatically divided into smaller chunks for efficient retrieval.

### 🧠 Semantic Search

Uses vector embeddings to find the most relevant content related to the user's query.

### 🤖 AI-Powered Question Answering

Ask questions in natural language and receive answers based on the PDF content.

### 📝 Document Summarization

Generate concise summaries of resumes, reports, research papers, and other documents.

### 📚 Source Citations

Displays page numbers used to generate answers for better transparency.

### 💬 Chat History

Maintains conversation history during the session.

### 🔄 Multiple PDF Support

Upload a new PDF and automatically replace the previous document context.

### ☁️ Deployment Ready

Can be deployed on Streamlit Community Cloud.

---

## 🏗️ Architecture

```text
PDF Upload
      │
      ▼
PDF Text Extraction
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Chroma Vector Database
      │
      ▼
Retriever
      │
      ▼
Gemini / Ollama
      │
      ▼
Answer Generation
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & RAG

* LangChain
* Google Gemini API
* Ollama (Optional)

### Vector Database

* ChromaDB

### Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2 Model

### PDF Processing

* PyPDF

---

## 📂 Project Structure

```text
pdf-rag-chatbot/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── utils/
    ├── pdf_loader.py
    ├── chunker.py
    ├── vector_store.py
    └── rag_chain.py
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/im-amanjai/pdf-rag-chatbot.git
```

```bash
cd pdf-rag-chatbot
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
LLM_PROVIDER=gemini
```

---

### 5. Run Application

```bash
streamlit run app.py
```

---

## 📖 How It Works

### Step 1

User uploads a PDF.

### Step 2

Text is extracted from all PDF pages.

### Step 3

Text is split into smaller chunks.

### Step 4

Each chunk is converted into vector embeddings.

### Step 5

Embeddings are stored in ChromaDB.

### Step 6

When the user asks a question:

* Relevant chunks are retrieved
* Context is sent to Gemini/Ollama
* AI generates an answer using only the retrieved content

### Step 7

The answer and source pages are displayed to the user.

---

## 🎯 Example Questions

### Resume

```text
What are the candidate's skills?
```

```text
What projects has the candidate worked on?
```

```text
What is the candidate's education background?
```

### Research Papers

```text
Summarize this document.
```

```text
What are the key findings?
```

```text
Explain the methodology used.
```

### Notes & Books

```text
Explain Chapter 1.
```

```text
What are the important concepts?
```

---

## 🔮 Future Improvements

* Multi-PDF Support
* PDF Highlighting
* Conversation Memory
* Hybrid Search
* FAISS Vector Store Support
* User Authentication
* Export Chat as PDF

---

## 👨‍💻 Author

**Aman Jaiswal**

* GitHub: https://github.com/im-amanjai
* LinkedIn: Add Your LinkedIn URL

---

## ⭐ If you found this project useful

Give this repository a star and support the project.
