# PDFs → Text → Chunks → Embeddings → Vector DB (persistent)

# User Question
#    + Chat History
#         ↓
# Retriever → Context → LLM → Answer + Sources

# pip install fastapi uvicorn langchain faiss-cpu pypdf sentence-transformers transformers torch python-multipart

rag_pdf_chat/
 ├── main.py
 ├── data/
 ├── vector_store/
