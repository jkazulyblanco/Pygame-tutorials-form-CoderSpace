# https://www.youtube.com/watch?v=lk1_h2_GLv8

import pygame, sys
from random import randint
from copy import deepcopy

# Global variables
RES = WIDTH, HEIGHT = 1280, 720
FPS = 10
TILE = 10
W, H = WIDTH // TILE, HEIGHT // TILE

# Global Setup
pygame.init()
surface = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()

# surfaces ========================================
# FILL ALL GRID WITH 0
next_field = [[0 for i in range(W)] for j in range(H)]

# FILL THE ACUTAL STATE WITH 1-0 RANDOMLY:
# current_field = [[randint(0, 1) for i in range(W)] for j in range(H)] # random
current_field = [[1 if i == W//2 or j == H//2 else 0 for i in range(W)] for j in range(H)] # Cross
# current_field = [[1 if not i % 9 else 0 for i in range(W)]for j in range(H)] # columns
# current_field = [[1 if not (2*i +j) % 4 else 0 for i in range(W)] for j in range(H)] # tuple, piramid
# current_field = [[1 if not (i*j) % 22 else 0 for i in range(W)] for j in range(H)] # tuple, tiles
# current_field = [[1 if not i % 7 else randint(0,1) for i in range(W)] for j in range(H)] # random


# Functions ======================================
def check_cell(current_field, x, y):
    count = 0
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            if current_field[j][i]:
                count += 1

    if current_field[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0

# Game Loop =======================================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # key Events =============================

    surface.fill('black')
    # Draw Grid
    color_grid = (23,23,23)
    [pygame.draw.line(surface, color_grid, (x,0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pygame.draw.line(surface, color_grid, (0,y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]
    
    # Draw Life
    for x in range(1, W-1):
        for y in range(1, H-1):
            if current_field[y][x]:
                pygame.draw.rect(surface, 'cyan', (x*TILE+2, y*TILE+2, TILE-2, TILE-2))
            next_field[y][x] = check_cell(current_field, x, y)

    current_field = deepcopy(next_field)

    pygame.display.flip()
    clock.tick(FPS)
    pygame.display.set_caption(f'fps: {clock.get_fps() :.0f}')