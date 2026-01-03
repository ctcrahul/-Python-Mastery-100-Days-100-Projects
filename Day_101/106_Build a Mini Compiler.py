# Project 106: Mini Programming Language Compiler
# Author: You

import re

# -----------------------------
# LEXER
# -----------------------------
TOKEN_SPEC = [
    ("NUMBER",   r"\d+"),
    ("ASSIGN",   r"="),
    ("PRINT",    r"print"),
    ("ID",       r"[a-zA-Z_]\w*"),
    ("PLUS",     r"\+"),
    ("SKIP",     r"[ \t]+"),
    ("NEWLINE",  r"\n"),
]
