# https://www.youtube.com/watch?v=lk1_h2_GLv8

import pygame, sys
from random import randint
from copy import deepcopy

# Numpy
import numpy as np
from numba import njit

# Global variables
RES = WIDTH, HEIGHT = 1280, 720
FPS = 30
TILE = 3
W, H = WIDTH // TILE, HEIGHT // TILE

# Global Setup
pygame.init()
surface = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()

# surfaces ========================================
next_field = np.array([[0 for i in range(W)] for j in range(H)])
# current_field = np.array([[randint(0, 1) for i in range(W)] for j in range(H)]) # random
# current_field = np.array([[1 if i == W//2 or j == H//2 else 0 for i in range(W)] for j in range(H)]) # Cross
# current_field = np.array([[1 if not (i*j) % 22 else 0 for i in range(W)] for j in range(H)]) # tuple, tiles

# numpy
current_field = np.array([[0 for i in range(W)] for j in range(H)])
for i in range(H):
    current_field[i][i+(W-H) //2] = 1
    current_field[H-i -1][i +(W-H) //2] = 1

# current_field = np.array([[1 if i == W//2 or j == H//2 else 0 for i in range(W)] for j in range(H)])


# Functions ======================================
@njit(fastmath= True)
def check_cells(current_field, next_field):
    res = []
    for x in range(W):
        for y in range(H):
            count = 0
            for j in range(y-1, y+2):
                for i in range(x-1, x+2):
                    if current_field[j % H][i % W] == 1:
                        count += 1
            
            if current_field[y][x] == 1:
                count -= 1
                if count == 2 or count == 3:
                    next_field[y][x] = 1
                    res.append((x,y))
                else:
                    next_field[y][x] = 0
            else:
                if count == 3:
                    next_field[y][x] = 1
                    res.append((x,y))
                else:
                    next_field[y][x]
    return next_field, res

# Game Loop =======================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key Events =============================

    surface.fill('black')
    # Draw Grid
    
    # Draw Life
    next_field, res = check_cells(current_field, next_field)
    [pygame.draw.rect(surface, 'cyan', (x*TILE+1, y*TILE+1, TILE-1, TILE-1)) for x,y in res]

    current_field = deepcopy(next_field)

    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption(f'fps: {clock.get_fps() :.0f}')