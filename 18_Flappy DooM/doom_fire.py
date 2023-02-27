import pygame
from random import randint
# much faster to draw particles
from pygame import gfxdraw
from settings import *

STEP_COLORS = 7

# color names 
# https://www.webucator.com/article/python-color-constants-module/

# COLORS = ['black','red','orange','yellow','white']
COLORS = ['black','olivedrab4','red','olivedrab2','white']
# COLORS = ['black','orchid4','orchid3','orchid2','white']

FIRE_TILES_X = 4
PIXEL_SIZE = 3
FIRE_WIDTH = WINDOW_WIDTH // (PIXEL_SIZE * FIRE_TILES_X)
FIRE_HEIGHT = WINDOW_HEIGHT // PIXEL_SIZE

class Doom_fire:
    def __init__(self, game):
        self.game = game
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surface = pygame.Surface([PIXEL_SIZE * FIRE_WIDTH, WINDOW_HEIGHT])
        self.fire_surface.set_colorkey('black')


    # Palette Blend colors --------------------------------
    @staticmethod
    def get_palette():
        palette = [(0,0,0)] # to store new colors
        for index_color, color in enumerate(COLORS[:-1]): # form black until yellow
            color_1 = color # get values from list colors
            color_2 = COLORS[index_color+1] # get values from list starting form red until white
            for step in range(STEP_COLORS):
                new_color = pygame.Color(color_1).lerp(color_2, (step+0.5) /STEP_COLORS)
                palette.append(new_color)
        return palette
    
    def draw_palette(self):
        size = 75
        for index, color in enumerate(self.palette):
            pygame.draw.rect(self.app.screen, color, (index*size, WINDOW_HEIGHT//2, size-5, size-5))

    # Fire effect ----------------------------------------
    def get_fire_array(self):
        # fill grid with 0 for x and y screen
        fire_array = [[0 for x in range(FIRE_WIDTH)] for y in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH): # for each value
            # asing the last color value except the last line
            fire_array[FIRE_HEIGHT-1][i] = len(self.palette) -1
        
        return fire_array

    def draw_fire(self):
        self.fire_surface.fill('black')
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.palette[color_index]
                    rect = (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                    gfxdraw.box(self.fire_surface, rect, color)

        for i in range(FIRE_TILES_X):
            self.game.screen.blit(self.fire_surface, (self.fire_surface.get_width()*i, 0))
    
    def do_fire(self):
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    rand_value = randint(0, 3)
                    self.fire_array[y-1][(x-rand_value+1)%FIRE_WIDTH] = color_index - rand_value %2
                else: # off the full black particles in top part
                    self.fire_array[y-1][x] = 0

    def update(self):
        self.do_fire()

    def draw(self):
        # self.draw_palette()
        self.draw_fire()
