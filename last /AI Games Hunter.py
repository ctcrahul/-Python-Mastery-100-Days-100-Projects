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

def draw():
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,255,0),(player_pos[0]*CELL,player_pos[1]*CELL,CELL,CELL))
    pygame.draw.rect(screen,(255,0,0),(ai_pos[0]*CELL,ai_pos[1]*CELL,CELL,CELL))
    pygame.draw.rect(screen,(255,255,0),(coin_pos[0]*CELL,coin_pos[1]*CELL,CELL,CELL))
    pygame.display.update()

def move_ai():
    global trained

    if trained and len(move_history) > 20:
        prediction = model.predict([move_history[-1]])[0]
        px, py = player_pos

        if prediction == 0:
            target = [px, py-1]
        elif prediction == 1:
            target = [px, py+1]
        elif prediction == 2:
            target = [px-1, py]
        else:
            target = [px+1, py]

        ai_pos[0] += np.sign(target[0]-ai_pos[0])
        ai_pos[1] += np.sign(target[1]-ai_pos[1])
    else:
        ai_pos[0] += np.sign(player_pos[0]-ai_pos[0])
        ai_pos[1] += np.sign(player_pos[1]-ai_pos[1])

def train_model():
    global trained
    if len(move_history) > 30:
        model.fit(move_history[:-1], labels[1:])
        trained = True

running = True
while running:
    clock.tick(10)

    prev = player_pos.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= 1
        move = 0
    elif keys[pygame.K_DOWN] and player_pos[1] < 19:
        player_pos[1] += 1
        move = 1
    elif keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 1
        move = 2
    elif keys[pygame.K_RIGHT] and player_pos[0] < 19:
        player_pos[0] += 1
        move = 3
    else:
        move = None

    if move is not None:
        move_history.append(prev)
        labels.append(move)
        train_model()

    move_ai()

    if player_pos == coin_pos:
        coin_pos = [random.randint(0,19), random.randint(0,19)]

    if player_pos == ai_pos:
        print("AI caught you!")
        running = False

    draw()

pygame.quit()
