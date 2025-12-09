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
