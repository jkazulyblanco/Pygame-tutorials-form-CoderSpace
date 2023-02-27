import os, sys
import pygame as pg
from random import choice, randrange

class Symbol:
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.speed = speed
        self.value = choice(green_katakana)
        self.interval = randrange(5, 30)

    def draw(self, color):
        # randomize the sybol
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
        
        # fall effect of the symbol
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
        surface.blit(self.value, (self.x, self.y))

class SymbolColumn:
    def __init__(self, x, y):
        self.column_height = randrange(8, 24)
        self.speed = randrange(2, 5)
        # colum of symbol
        self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, - FONT_SIZE)]

    def draw(self):
        # different colors
        [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]

# old method for center screen
os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1280, 720
FONT_SIZE = 40
alpha_value = 0

# pygame setup ======================================
pg.init()
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()
# blur effect
surface = pg.Surface(RES)
surface.set_alpha(alpha_value)

# katakana from hexadecimal values
katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
# load font
font = pg.font.Font('font/MS Mincho.ttf', FONT_SIZE, bold= True)
green_katakana = [font.render(char, True, (40, randrange(160, 256), 40)) for char in katakana]
# font color
lightgreen_katakana = [font.render(char, True, pg.Color('lightgreen')) for char in katakana]

# Instance of class
symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Draw ------------------------
    screen.blit(surface, (0, 0))
    surface.fill(pg.Color('black'))

    # many colums
    [symbol_column.draw() for symbol_column in symbol_columns]

    if not pg.time.get_ticks() % 20 and alpha_value < 170:
        alpha_value += 6
        surface.set_alpha(alpha_value)

    # pygame setup ------------------------
    pg.display.flip()
    clock.tick(60)
    pg.display.set_caption(f'FPS: {clock.get_fps() :.0f}')
