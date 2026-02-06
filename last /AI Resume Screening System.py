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

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        job_desc = request.form["job_desc"]
        resumes = request.files.getlist("resumes")

        documents = [job_desc]
        filenames = []

        for resume in resumes:
            path = os.path.join(UPLOAD_FOLDER, resume.filename)
            resume.save(path)
            text = extract_text(path)
            documents.append(text)
            filenames.append(resume.filename)

        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(documents)

        scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        for name, score in zip(filenames, scores):
            results.append((name, round(score * 100, 2)))

        results.sort(key=lambda x: x[1], reverse=True)

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(debug=True)

