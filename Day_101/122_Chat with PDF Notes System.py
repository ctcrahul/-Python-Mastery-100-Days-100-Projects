# PDF → Text → Chunks → Embeddings → Vector Store
#                                  ↓
# User Question → Similarity Search → LLM → Answer


# chat_with_pdf/
#  ├── app.py
#  ├── templates/
#  │    └── index.html
#  ├── uploads/



###################### app.py

from flask import Flask, render_template, request
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from pypdf import PdfReader
from transformers import pipeline
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vector_db = None

# -----------------------------
# LOAD PDF
# -----------------------------
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# -----------------------------
# CREATE VECTOR STORE
# -----------------------------
def create_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_texts(chunks, embeddings)

# -----------------------------
# LOAD LLM
# -----------------------------
def load_llm():
    generator = pipeline(
        "text-generation",
        model="google/flan-t5-base",
        max_length=256
    )
    return HuggingFacePipeline(pipeline=generator)

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    global vector_db

    answer = ""

    if request.method == "POST":
        if "pdf" in request.files:
            pdf = request.files["pdf"]
            path = os.path.join(UPLOAD_FOLDER, pdf.filename)
            pdf.save(path)

            text = load_pdf(path)
            vector_db = create_vector_store(text)

        if "question" in request.form and vector_db:
            llm = load_llm()
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=vector_db.as_retriever()
            )
            answer = qa.run(request.form["question"])

    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)



################# templates/index.html

<!DOCTYPE html>
<html>
<head>
    <title>Chat with PDF</title>
</head>
<body>
    <h2>Chat with PDF Notes</h2>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="pdf" required>
        <button type="submit">Upload PDF</button>
    </form>

    <hr>

    <form method="POST">
        <input type="text" name="question" placeholder="Ask a question..." required>
        <button type="submit">Ask</button>
    </form>

    <h3>Answer:</h3>
    <p>{{ answer }}</p>
</body>
</html>

