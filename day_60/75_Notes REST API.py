"""
Project 75 — Notes REST API
Run: python notes_api.py
Requirements: Python 3.8+, Flask
Install: pip install Flask

Features:
- Create, read, update, delete notes
- Search notes by text
- Pagination (page, per_page)
- Export notes as CSV
- Minimal validation and clear JSON responses
"""

from flask import Flask, request, jsonify, g, send_file, abort
import sqlite3
from datetime import datetime
import csv
import io
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")
APP = Flask(__name__)


# ---------- Database helpers ----------
def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db
    def init_db():
    db = sqlite3.connect(DB_PATH)
    cur = db.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    
    db.commit()
    db.close()


@APP.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()


# ---------- Utility ----------
def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def note_row_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "body": row["body"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }
# ---------- Routes ----------
@APP.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@APP.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    title = (data.get("title") or "").strip()
    body = (data.get("body") or "").strip()

    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not body:
        return jsonify({"error": "Body is required"}), 400

    db = get_db()
    cur = db.cursor()
    ts = now_iso()
    cur.execute(
        "INSERT INTO notes (title, body, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (title, body, ts, ts),
    )
