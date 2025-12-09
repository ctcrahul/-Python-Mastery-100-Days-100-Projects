"""
Project 82 — Mini Relational Query Engine (SQL-Lite Interpreter)
This is not using SQLite. 
You're building a tiny relational engine yourself.

Supported:
    CREATE table col1 col2 col3
    INSERT table val1 val2 val3
    SELECT table
    SELECT table WHERE col == value
"""

import shlex


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns          # list of column names
        self.rows = []                  # list of dicts
        self.indexes = {}               # col_name -> {value: [row_ids]}

    def insert(self, values):
        if len(values) != len(self.columns):
            return "ERR: column count mismatch"

        row = dict(zip(self.columns, values))
        row_id = len(self.rows)
        self.rows.append(row)
        # update indexes
        for col, idx in self.indexes.items():
            value = row[col]
            idx.setdefault(value, []).append(row_id)

        return "OK"

    def create_index(self, col):
        if col not in self.columns:
            return "ERR: no such column"

        idx = {}
        for i, row in enumerate(self.rows):
            value = row[col]
            idx.setdefault(value, []).append(i)

        self.indexes[col] = idx
        return f"Index created on {col}"

    def select_all(self):
        return self.rows

    def select_where(self, col, value):
        if col in self.indexes:
            # indexed lookup
            row_ids = self.indexes[col].get(value, [])
            return [self.rows[i] for i in row_ids]

        # fallback scan
        return [r for r in self.rows if r.get(col) == value]


class Engine:
    def __init__(self):
        self.tables = {}

    def execute(self, command):
        parts = shlex.split(command)
        if not p
