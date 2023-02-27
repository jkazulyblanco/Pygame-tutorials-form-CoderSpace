import pygame


def quads_area(atlas, x, y, width, height):
    quad_rect = pygame.Rect(x, y, width, height)
    quad_atlas = atlas.subsurface(quad_rect)
    return quad_atlas

RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
# RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 900

SPEED = 200

NUM_SPRITES_PER_CLICK = 50

# Cahche trick
NUM_ANGLES = 180

# arcade
SPRITE_DIR_PATH = 'sprites'