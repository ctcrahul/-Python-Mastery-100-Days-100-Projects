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

        # bias
        self.b = random.uniform(-1, 1)

        self.lr = 0.1

    def forward(self, x1, x2):
        self.z = x1 * self.w1 + x2 * self.w2 + self.b
        self.output = sigmoid(self.z)
        return self.output

    def backward(self, x1, x2, y):
        error = y - self.output
        d_output = error * sigmoid_derivative(self.output)

        self.w1 += self.lr * d_output * x1
        self.w2 += self.lr * d_output * x2
        self.b += self.lr * d_output

    def train(self, data, epochs=5000):
        for _ in range(epochs):
            x1, x2, y = random.choice(data)
            self.forward(x1, x2)
            self.backward(x1, x2, y)

    def predict(self, x1, x2):
        return round(self.forward(x1, x2), 3)

# -----------------------------
# DATASET (AND GATE)
# -----------------------------
training_data = [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1)
]

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    nn = NeuralNetwork()
    nn.train(training_data)

    print("Results after training:\n")
    for x1, x2, _ in training_data:
        print(f"{x1} AND {x2} = {nn.predict(x1, x2)}")
