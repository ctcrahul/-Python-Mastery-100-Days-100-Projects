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
def lex(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for tok_type, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if tok_type not in ("SKIP", "NEWLINE"):
                    tokens.append((tok_type, text))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f"Illegal character: {code[pos]}")
    return tokens
# -----------------------------
# PARSER / INTERPRETER
# -----------------------------
class Interpreter:
    def __init__(self):
        self.vars = {}

    def run(self, tokens):
        i = 0
        while i < len(tokens):
            tok, val = tokens[i]

            if tok == "ID" and tokens[i+1][0] == "ASSIGN":
                var = val
                expr = tokens[i+2:i+5]
                result = self.eval_expr(expr)
                self.vars[var] = result
                i += 5
