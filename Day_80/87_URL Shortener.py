"""
Project 87 — URL Shortener (Flask + SQLite)

Routes:
POST /shorten   { "url": "https://example.com" }
GET  /<code>    -> redirect
GET  /stats/<code>
"""

import sqlite3
import string
import random
from flask import Flask, request, redirect, jsonify

DB = "urls.db"
BASE62 = string.ascii_letters + string.digits

app = Flask(__name__)


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0
            )
        """)

def generate_code(length=6):
    return "".join(random.choice(BASE62) for _ in range(length))


def save_url(code, url):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "INSERT INTO urls (code, url) VALUES (?, ?)",
            (code, url)
        )


def get_url(code):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute(
            "SELECT url, clicks FROM urls WHERE code=?",
            (code,)
        )
        return cur.fetchone()


def increment_click(code):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE code=?",
            (code,)
        )

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL required"}), 400

    while True:
        code = generate_code()
        if not get_url(code):
            break

    save_url(code, url)
    return jsonify({"short_url": f"http://127.0.0.1:5000/{code}"})


@app.route("/<code>")
def redirect_url(code):
    record = get_url(code)
    if not record:
        return jsonify({"error": "Not found"}), 404

    url, _ = record
    increment_click(code)
    return redirect(url)
