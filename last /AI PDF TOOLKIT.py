# ==========================================
# AI PDF TOOLKIT - SINGLE FILE VERSION
# ==========================================
# Features:
# Merge PDF
# Split PDF
# Compress PDF
# Add Watermark
# Smart Summary (Basic AI Ready)
# ==========================================

from flask import Flask, request, send_file, render_template_string
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import pdfplumber
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= MERGE PDF =================
def merge_pdfs(files, output_path):
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    merger.write(output_path)
    merger.close()

# ================= SPLIT PDF =================
def split_pdf(file, start, end, output_path):
    reader = PdfReader(file)
    writer = PdfWriter()

    for i in range(start-1, end):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

# ================= COMPRESS PDF =================
def compress_pdf(file, output_path):
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata({"Compressed": "True"})

    with open(output_path, "wb") as f:
        writer.write(f)

# ================= WATERMARK =================
def add_watermark(file, text, output_path):
    watermark_path = "watermark.pdf"

    c = canvas.Canvas(watermark_path)
    c.drawString(200, 500, text)
    c.save()

    watermark = PdfReader(watermark_path)
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.merge_page(watermark.pages[0])
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

# ================= PDF SUMMARY =================
def summarize_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    summary = text[:500]  # Basic Summary Logic
    return summary

# ================= ROUTES =================

HTML = """
<h2>AI PDF TOOLKIT</h2>

<h3>Merge PDFs</h3>
<form method=post action="/merge" enctype=multipart/form-data>
<input type=file name=files multiple>
<input type=submit value=Merge>
</form>

<h3>Split PDF</h3>
<form method=post action="/split" enctype=multipart/form-data>
<input type=file name=file>
Start Page: <input type=number name=start>
End Page: <input type=number name=end>
<input type=submit value=Split>
</form>

<h3>Compress PDF</h3>
<form method=post action="/compress" enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Compress>
</form>

<h3>Add Watermark</h3>
<form method=post action="/watermark" enctype=multipart/form-data>
<input type=file name=file>
Watermark Text: <input type=text name=text>
<input type=submit value=Add>
</form>

<h3>Summarize PDF</h3>
<form method=post action="/summary" enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Summarize>
</form>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/merge", methods=["POST"])
def merge():
    files = request.files.getlist("files")
    paths = []
    for f in files:
        path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(path)
        paths.append(path)

    output = os.path.join(UPLOAD_FOLDER, "merged.pdf")
    merge_pdfs(paths, output)
    return send_file(output)

@app.route("/split", methods=["POST"])
def split():
    file = request.files["file"]
    start = int(request.form["start"])
    end = int(request.form["end"])

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    output = os.path.join(UPLOAD_FOLDER, "split.pdf")
    split_pdf(path, start, end, output)
    return send_file(output)

@app.route("/compress", methods=["POST"])
def compress():
    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    output = os.path.join(UPLOAD_FOLDER, "compressed.pdf")
    compress_pdf(path, output)
    return send_file(output)

@app.route("/watermark", methods=["POST"])
def watermark():
    file = request.files["file"]
    text = request.form["text"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    output = os.path.join(UPLOAD_FOLDER, "watermarked.pdf")
    add_watermark(path, text, output)
    return send_file(output)

@app.route("/summary", methods=["POST"])
def summary():
    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    summary = summarize_pdf(path)
    return f"<h3>Summary:</h3><p>{summary}</p>"

if __name__ == "__main__":
    app.run(debug=True)
