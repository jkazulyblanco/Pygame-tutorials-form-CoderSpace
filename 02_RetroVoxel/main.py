import sys
import pygame as pg
from player import Player
from voxel_render import VoxelRender

class App:
    def __init__(self):
        self.res = self.width, self.height = (800, 600)
        self.screen = pg.display.set_mode(self.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.player = Player()
        self.voxel_render = VoxelRender(self)

    def update(self):
        self.player.update()
        self.voxel_render.update()

    def draw(self):
        self.voxel_render.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.update()
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