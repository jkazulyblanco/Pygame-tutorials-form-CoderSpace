import pygame as pg
from game_objects import *
import sys 

class Game:
    def __init__(self):
        pg.init()
        self.WINDOW_SIZE = 700
        self.TILE_SIZE = 35
        # create a square window with the same amount of pixels x = y
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.new_game()

    def draw_grid(self):
        # Vertical lines
        [pg.draw.line(self.screen, [35] * 3, (x, 0), (x, self.WINDOW_SIZE))
                        for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        # horizontal lines
        [pg.draw.line(self.screen, [35] * 3, (0, y), (self.WINDOW_SIZE, y))
                        for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        
    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def new_game(self):
        self.snake = Snake(self)
        self.food = Food(self)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        self.snake.draw()
    
    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.clock.tick(60)
            pg.display.set_caption(f'FPS: {self.clock.get_fps():.0f}')
            # snake control
            self.snake.control(event)
            

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()