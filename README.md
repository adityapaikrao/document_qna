# Document Q&A RAG Bot

A Streamlit-based web application that allows users to upload PDF documents and ask questions based on their content. The application employs Retrieval-Augmented Generation (RAG) techniques to provide contextually accurate answers using semantic search and use of local Large Language Models (LLMs) via Ollama.

---

## Features

- **PDF Upload:** Upload a PDF file directly through the app.
- **Semantic Chunking:** Splits the document into meaningful chunks for efficient retrieval.
- **Local LLM Integration:** Uses local LLMs for inference, ensuring data privacy.
- **ChromaDB Backend:** A Vector DB to enable fast and accurate semantic search.

---

## Getting Started

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/adityapaikrao/document_qna.git
   cd document_qna
   ```
2. **Install dependencies**
    ```
    pip install -r requirements.in
    ```

3. Run the App!
  ```
  streamlit run.py
  ```


