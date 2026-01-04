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
