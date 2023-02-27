import pygame as pg
import sys
from random import random
from collections import deque


cols, rows = 25, 15
TILE = 40

def get_rect(x, y):
    return x*TILE+1, y*TILE+1, TILE-2, TILE-2

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode([cols*TILE, rows*TILE], vsync=1)

# Surfaces ==============================================
# create random grid with values 1 or 0
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]


# Game Loop =============================================
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # Key events ====================================

    # Draw - Update =====================================
    screen.fill('black')

    [[pg.draw.rect(screen, 'darkorange', get_rect(x,y), border_radius=TILE//5)
    for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

    pg.display.update()
    clock.tick(7)
    pg.display.set_caption(f'fps: {clock.get_fps() :.0f}')

