# PDFs → Text → Chunks → Embeddings → Vector DB (persistent)

# User Question
#    + Chat History
#         ↓
# Retriever → Context → LLM → Answer + Sources

# pip install fastapi uvicorn langchain faiss-cpu pypdf sentence-transformers transformers torch python-multipart

# rag_pdf_chat/
#  ├── main.py
#  ├── data/
#  ├── vector_store/


  ##############                Main .py

  from fastapi import FastAPI, UploadFile, Form
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from pypdf import PdfReader
from transformers import pipeline
import os

app = FastAPI()

DATA_DIR = "data"
DB_DIR = "vector_store"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

# -----------------------------
# GLOBAL OBJECTS
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

vector_db = None

# -----------------------------
# UTILITIES
# -----------------------------
def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def load_llm():
    gen = pipeline(
        "text-generation",
        model="google/flan-t5-base",
        max_length=256
    )
    return HuggingFacePipeline(pipeline=gen)

# -----------------------------
# ROUTES
# -----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile):
    global vector_db

    path = os.path.join(DATA_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(await file.read())

    text = read_pdf(path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)

    if vector_db is None:
        vector_db = FAISS.from_texts(chunks, embeddings)
    else:
        vector_db.add_texts(chunks)

    vector_db.save_local(DB_DIR)

    return {"status": "PDF indexed successfully"}

@app.post("/chat")
async def chat(question: str = Form(...)):
    global vector_db

    if vector_db is None:
        return {"error": "Upload PDFs first"}

    llm = load_llm()

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_db.as_retriever(),
        memory=memory,
        return_source_documents=True
    )

    result = qa({"question": question})

    sources = list(set(
        doc.metadata.get("source", "PDF")
        for doc in result["source_documents"]
    ))

    return {
        "answer": result["answer"],
        "sources": sources
    }
