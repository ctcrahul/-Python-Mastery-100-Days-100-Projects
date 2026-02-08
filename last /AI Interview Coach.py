from flask import Flask, request, render_template_string
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# ------------------ DATA ------------------
ROLES = {
    "Data Analyst": [
        "Explain a data-driven decision you made.",
        "How do you handle missing data?",
        "What is overfitting?"
    ],
    "ML Engineer": [
        "Explain bias-variance tradeoff.",
        "How would you deploy an ML model?",
        "What is model drift?"
    ]
}

IDEAL_ANSWERS = {
    "Explain a data-driven decision you made.": "business impact metrics analysis outcome",
    "How do you handle missing data?": "imputation deletion distribution statistics",
    "What is overfitting?": "model memorizes training data poor generalization",
    "Explain bias-variance tradeoff.": "underfitting overfitting balance error",
    "How would you deploy an ML model?": "api docker monitoring versioning",
    "What is model drift?": "data distribution changes performance degradation"
}

# ------------------ LOGIC ------------------
def evaluate_answer(answer, reference):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, reference])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    length_score = min(len(answer.split()) / 80, 1.0)
    final_score = round((similarity * 0.7 + length_score * 0.3) * 100, 2)

    return final_score, similarity

def generate_feedback(answer, score):
    doc = nlp(answer)
    filler_words = [t.text for t in doc if t.text.lower() in ["um", "uh", "like"]]

    feedback = []
    if score < 40:
        feedback.append("Weak answer. No structure, no clarity.")
    elif score < 70:
        feedback.append("Average answer. Improve depth and examples.")
    else:
        feedback.append("Strong answer. Clear and relevant.")

    if len(answer.split()) < 30:
        feedback.append("Answer is too short. Expand with reasoning.")
    if filler_words:
        feedback.append(f"Remove filler words: {set(filler_words)}")

    return " ".join(feedback)

# ------------------ UI ------------------
HTML = """
<h2>AI Interview Coach</h2>
<form method="post">
    <label>Role</label><br>
    <select name="role" onchange="this.form.submit()">
        {% for r in roles %}
            <option value="{{r}}" {% if r == role %}selected{% endif %}>{{r}}</option>
        {% endfor %}
    </select><br><br>

    <label>Question</label><br>
    <select name="question">
        {% for q in questions %}
            <option value="{{q}}">{{q}}</option>
        {% endfor %}
    </select><br><br>

    <textarea name="answer" rows="6" cols="80" placeholder="Type your answer here..."></textarea><br><br>
    <button type="submit">Evaluate</button>
</form>

{% if score %}
<hr>
<h3>Score: {{score}} / 100</h3>
<p><b>Feedback:</b> {{feedback}}</p>
{% endif %}
"""

# ------------------ ROUTE ------------------
@app.route("/", methods=["GET", "POST"])
def index():
    role = request.form.get("role", "Data Analyst")
    questions = ROLES[role]

    score = None
    feedback = None

    if request.method == "POST" and "answer" in request.form:
        question = request.form["question"]
        answer = request.form["answer"]

        score, _ = evaluate_answer(answer, IDEAL_ANSWERS[question])
        feedback = generate_feedback(answer, score)
    return render_template_string(
        HTML,
        roles=ROLES.keys(),
        role=role,
        questions=questions,
        score=score,
        feedback=feedback
    )

if __name__ == "__main__":
    app.run(debug=True)
