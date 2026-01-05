import random
import math

# -----------------------------
# ACTIVATION FUNCTIONS
# -----------------------------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

# -----------------------------
# NEURAL NETWORK
# -----------------------------
class NeuralNetwork:
    def __init__(self):
        # weights
        self.w1 = random.uniform(-1, 1)
        self.w2 = random.uniform(-1, 1)
        self.w3 = random.uniform(-1, 1)
