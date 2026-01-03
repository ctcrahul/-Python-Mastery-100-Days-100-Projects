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
                i += 5            elif tok == "PRINT":
                expr = tokens[i+1:i+4]
                result = self.eval_expr(expr)
                print(result)
                i += 4

            else:
                raise SyntaxError("Invalid syntax")

    def eval_expr(self, expr):
        if len(expr) == 1:
            return self.resolve(expr[0])

        left = self.resolve(expr[0])
        right = self.resolve(expr[2])
        return left + right

    def resolve(self, token):
        tok, val = token
        if tok == "NUMBER":
            return int(val)
        if tok == "ID":
            return self.vars.get(val, 0)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Mini Language (type 'exit' to quit)")
    interpreter = Interpreter()

    while True:
        code = input(">>> ")
        if code == "exit":
            break

        tokens = lex(code)
        interpreter.run(tokens)
