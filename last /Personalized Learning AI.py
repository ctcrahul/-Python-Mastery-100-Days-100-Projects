# pip install flask scikit-learn spacy
# python -m spacy download en_core_web_sm

from flask import Flask, request, render_template_string
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Learning Content
# -----------------------------
TOPICS = {
    "Python Basics": {
        "easy": "Explain what a variable is in Python.",
        "medium": "Difference between list and tuple.",
        "hard": "Explain Python memory management."
    },
    "Machine Learning": {
        "easy": "What is supervised learning?",
        "medium": "Explain bias vs variance.",
        "hard": "How does gradient descent work?"
    }
}

IDEAL_ANSWERS = {
    "Explain what a variable is in Python.": "stores data value memory",
    "Difference between list and tuple.": "mutable immutable performance",
    "Explain Python memory management.": "heap garbage collection reference",
    "What is supervised learning?": "labeled data prediction",
    "Explain bias vs variance.": "underfitting overfitting tradeoff",
    "How does gradient descent work?": "optimization loss function learning rate"
}

USER_STATE = {
    "level": "easy",
    "history": []
}

# -----------------------------
# Core AI Logic
# -----------------------------
def evaluate_answer(answer, reference):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, reference])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity * 100, 2)
        return score

def update_level(score):
    if score < 40:
        return "easy"
    elif score < 70:
        return "medium"
    else:
        return "hard"

# -----------------------------
# UI
# -----------------------------
HTML = """
<h2>Personalized Learning AI</h2>

<form method="post">
<label>Topic</label><br>
<select name="topic">
{% for t in topics %}
<option value="{{t}}">{{t}}</option>
{% endfor %}
</select><br><br>

<label>Question</label><br>
<p><b>{{question}}</b></p>

<textarea name="answer" rows="6" cols="80" placeholder="Type your answer..."></textarea><br><br>
<button type="submit">Submit</button>
</form>

{% if score %}
<hr>
<h3>Score: {{score}}</h3>
<p><b>New Difficulty Level:</b> {{level}}</p>
{% endif %}
"""


# -----------------------------
# Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    topic = request.form.get("topic", "Python Basics")
    level = USER_STATE["level"]
    question = TOPICS[topic][level]

    score = None

    if request.method == "POST":
        answer = request.form["answer"]
        score = evaluate_answer(answer, IDEAL_ANSWERS[question])
        new_level = update_level(score)

        USER_STATE["level"] = new_level
        USER_STATE["history"].append((topic, question, score))

        level = new_level

    return render_template_string(
        HTML,
        topics=TOPICS.keys(),
        question=question,
        score=score,
        level=level
    )

if __name__ == "__main__":
    app.run(debug=True)
