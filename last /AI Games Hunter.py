import pygame
import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID = 20
CELL = WIDTH // GRID

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Games Hunter")

clock = pygame.time.Clock()

player_pos = [1, 1]
ai_pos = [18, 18]
coin_pos = [random.randint(0,19), random.randint(0,19)]

move_history = []
labels = []

model = DecisionTreeClassifier()
trained = False
