import random

# -----------------------------
# ENVIRONMENT
# -----------------------------
GRID_SIZE = 3
START = (0, 0)
GOAL = (2, 2)
TRAP = (1, 1)

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]

# -----------------------------
# Q-TABLE
# -----------------------------
Q = {}
def get_q(state, action):
    return Q.get((state, action), 0.0)

def set_q(state, action, value):
    Q[(state, action)] = value

# -----------------------------
# ENV STEP
# -----------------------------
def step(state, action):
    x, y = state

    if action == "UP":
        x -= 1
    elif action == "DOWN":
        x += 1
    elif action == "LEFT":
        y -= 1
    elif action == "RIGHT":
        y += 1
