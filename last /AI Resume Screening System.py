AI Resume Screening System

from flask import Flask, request, render_template_string
import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!doctype html>
<title>AI Resume Screening</title>
<h2>AI Resume Screening System</h2>

<form method=post enctype=multipart/form-data>
  <label>Job Description</label><br>
  <textarea name=job_desc rows=6 cols=80 required></textarea><br><br>

  <label>Upload Resumes (PDF or TXT)</label><br>
  <input type=file name=resumes multiple required><br><br>

  <input type=submit value="Analyze">
</form>

{% if results %}
<h3>Results</h3>
<table border="1" cellpadding="8">
<tr><th>Resume</th><th>Match Score (%)</th></tr>
{% for r in results %}
<tr><td>{{ r[0] }}</td><td>{{ r[1] }}</td></tr>
{% endfor %}
</table>
{% endif %}
"""
