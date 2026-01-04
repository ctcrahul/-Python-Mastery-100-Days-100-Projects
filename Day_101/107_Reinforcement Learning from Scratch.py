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
  for ep in range(episodes):
        state = START

        while True:
            action = choose_action(state, epsilon)
            next_state, reward, done = step(state, action)

            old_q = get_q(state, action)
            next_max = max(get_q(next_state, a) for a in ACTIONS)

            new_q = old_q + alpha * (reward + gamma * next_max - old_q)
            set_q(state, action, new_q)

            state = next_state
            if done:
                break

        epsilon = max(0.01, epsilon * 0.995)

    print("Training complete.")

# -----------------------------
# TEST AGENT
# -----------------------------
def test():
    state = START
    path = [state]

    while state != GOAL:
        action = choose_action(state, 0)
        state, _, _ = step(state, action)
        path.append(state)

        if len(path) > 20:
            break

    print("Learned path:", path)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    train()
    test()
