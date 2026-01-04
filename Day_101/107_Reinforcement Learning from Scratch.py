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
    x = max(0, min(GRID_SIZE - 1, x))
    y = max(0, min(GRID_SIZE - 1, y))

    new_state = (x, y)

    if new_state == GOAL:
        return new_state, 10, True
    if new_state == TRAP:
        return new_state, -10, True

    return new_state, -1, False

# -----------------------------
# POLICY (ε-greedy)
# -----------------------------
def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS)

    qs = [get_q(state, a) for a in ACTIONS]
    return ACTIONS[qs.index(max(qs))]

# -----------------------------
# TRAINING LOOP
# -----------------------------
def train(episodes=500):
    alpha = 0.1     # learning rate
    gamma = 0.9     # discount factor
    epsilon = 1.0
