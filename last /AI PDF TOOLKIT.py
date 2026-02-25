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
