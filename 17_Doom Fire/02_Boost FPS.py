import pygame, sys
from random import randint
# much faster to draw particles
from pygame import gfxdraw 

RES = WIDTH, HEIGHT = 1280, 720

LERP_COLORS = 10
COLORS = ['black','red','orange','yellow','white']

FIRE_TILES_X = 4
PIXEL_SIZE = 3
FIRE_WIDTH = WIDTH // (PIXEL_SIZE * FIRE_TILES_X)
FIRE_HEIGHT = HEIGHT // PIXEL_SIZE

class Doom_fire:
    def __init__(self, app):
        self.app = app
        self.palette = self.get_palette()
        self.fire_array = self.get_fire_array()
        self.fire_surface = pygame.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])
        self.fire_surface.set_colorkey('black')

        # appear logo of DooM
        self.logo = pygame.image.load('logo.png').convert_alpha()
        self.logo = pygame.transform.scale2x(self.logo)
        self.logo_x = WIDTH//2 -self.logo.get_width()//2
        self.logo_y = HEIGHT//4 -self.logo.get_height()//2
        self.logo_start_y = HEIGHT

    def draw_logo(self):
        if self.logo_start_y > self.logo_y:
            self.logo_start_y -= 1
        self.app.screen.blit(self.logo, (self.logo_x, self.logo_start_y))


    # Palette Blend colors --------------------------------
    @staticmethod
    def get_palette():
        palette = [(0,0,0)] # to store new colors
        for index_color, color in enumerate(COLORS[:-1]): # form black until yellow
            color_1 = color # get values from list colors
            color_2 = COLORS[index_color+1] # get values from list starting form red until white
            for step in range(LERP_COLORS):
                new_color = pygame.Color(color_1).lerp(color_2, (step+0.5) /LERP_COLORS)
                palette.append(new_color)
        return palette
    
    def draw_palette(self):
        size = 75
        for index, color in enumerate(self.palette):
            pygame.draw.rect(self.app.screen, color, (index*size, HEIGHT//2, size-5, size-5))

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

        for i in range(FIRE_TILES_X-1):
            self.app.screen.blit(self.fire_surface, (self.fire_surface.get_width()*i, 0))
    
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
        self.draw_logo()
        # self.draw_palette()
        self.draw_fire()


# MAIN CLASS ==============================================
class pygame_main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES, vsync=1)
        self.clock = pygame.time.Clock()
        # game setup ------------------------------------
        self.doom_fire = Doom_fire(self)

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
        pygame.display.set_caption(f'{self.clock.get_fps():.0f}')
        # Doom fire -------------------------------------
        self.doom_fire.update()

    def draw(self):
        self.screen.fill('black')
        # Doom fire --------------------------------------
        self.doom_fire.draw()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw()
            self.update()

if __name__ == '__main__':
    app = pygame_main()
    app.run()

