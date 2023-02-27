import pygame as pg
import math, sys

class Cardioid:
    def __init__(self, app):
        self.app = app
        # circle radius
        self.radius = 300 
        # lines to draw
        self.num_lines = 200 
        # center the image on screen, 0 and 1
        self.translate = self.app.screen.get_width() // 2, self.app.screen.get_height() // 2
        # for color gradient
        self.counter, self.inc = 0, 0.01

    def get_color(self):
        self.counter += self.inc
        self.counter, self.inc = (self.counter, self.inc) if 0 < self.counter < 1 else (
            max(min(self.counter, 1), 0), -self.inc)
        # blend colors
        return pg.Color('red').lerp('green', self.counter)


    def draw(self):
        # hearth beating effect
        time = pg.time.get_ticks()
        self.radius = 250 + 20 * abs(math.sin(time * 0.004) - 0.5)

        # animation effect
        factor = 1 + 0.0001 * time

        # draw loop by number of lines
        for i in range(self.num_lines):
            # calculate where the first point is located
            theta = (2 * math.pi / self.num_lines) * i
            # calculate the coordinates of the first point
            x1 = int(self.radius * math.cos(theta)) + self.translate[0]
            y1 = int(self.radius * math.sin(theta)) + self.translate[1]
            # calculate the coordinates of the second point
            x2 = int(self.radius * math.cos(factor * theta)) + self.translate[0]
            y2 = int(self.radius * math.sin(factor * theta)) + self.translate[1]
            # conect points
            pg.draw.aaline(self.app.screen, self.get_color(), (x1, y1), (x2, y2))

# Application class for Pygame
class App:
    # window resolution
    def __init__(self):
        self.screen = pg.display.set_mode([1280, 720])
        self.clock = pg.time.Clock()
        self.cardioid = Cardioid(self) # call

    # update and draw on the screen
    def draw(self):
        self.screen.fill('black')
        self.cardioid.draw() # call
        pg.display.flip()

    # launch, render method is call
    def run(self):
        while True:
            self.draw()
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.clock.tick(60)
            pg.display.set_caption(f'FPS: {self.clock.get_fps():.0f}')

if __name__ == '__main__':
    app = App()
    app.run()