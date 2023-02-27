import pygame as pg
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3
import sys

# ti.vulkan only work
ti.init(arch=ti.vulkan) # initialize taichi
# vectors to work whit numpy
RES = WIDTH, HEIGHT = vec2(800, 600)
# load texture power of two
# texture res - 2^n x 2^n (512 x 512, 1024 x 1024, ...)
texture = pg.image.load('img/lava.jpg')
texture_size = texture.get_size()[0]
# texture color mormalization 0 - 255 --> 0.0 - 1.0
texture_array = pg.surfarray.array3d(texture).astype(np.float32) / 255

@ti.data_oriented # taichi
class PyShader:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((WIDTH, HEIGHT, 3), [0, 0, 0], np.uint8)
        # taichi fields # taichi works with this data
        self.screen_field = ti.Vector.field(3, ti.uint8, (WIDTH, HEIGHT))
        self.texture_field = ti.Vector.field(3, ti.float32, texture.get_size())
        self.texture_field.from_numpy(texture_array)
    
    @ti.kernel # parallel computing method taichi
    def render(self, time: ti.float32):
        # fragment shader imitation
        for frag_coord in ti.grouped(self.screen_field):
            # normalized pixel colors, invert X, Y coordinate like love2d to normal coordinates
            #uv = frag_coord / RES
            #col = 0.5 + 0.5 * ts.cos(time + vec3(uv.x, uv.y, uv.x) + vec3(0.0, 2.0, 4.0))
            # coordinates origin to center of the screen
            uv = (frag_coord - 0.5 * RES) / RES.y
            col = vec3(0.0)
            # smooth movement
            uv += vec2(0.2 * ts.sin(time / 2), 0.3 * ts.cos(time /3))
            # polar coords
            phi = ts.atan(uv.y, uv.x)
            rho = ts.length(uv) # round tunnel
            # rho = pow(pow(uv.x ** 2, 4) + pow(uv.y ** 2, 4), 0.125) # square tunnel
            #col += vec3(phi) # phi 
            #col += vec3(phi / (2 * ts.pi) + 0.5) # phi 0 - 1
            #col += vec3(rho) # gradient circular
            st = vec2(phi / ts.pi * 2, 0.25 / rho)
            #st.x += time / 14 # rotation
            st.y += time / 2 # movement
            col += self.texture_field[int(st * texture_size)]
            # fade end of tunnel turning black
            col *= rho + 0.2
            # light at the end of the tunnel
            col += 0.1 / rho * vec3(0.4, 0.2, 0.1)

            col = ts.clamp(col, 0.0, 1.0)
            self.screen_field[frag_coord.x, RES.y - frag_coord.y] = col * 255

    def update(self):
        time = pg.time.get_ticks() * 1e-03 # time in sec
        self.render(time)
        self.screen_array = self.screen_field.to_numpy()

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES, pg.SCALED)
        self.clock = pg.time.Clock()
        # instance of the class
        self.shader = PyShader(self)
        

    def run(self):
        while True:
            # instance of the class
            self.shader.run()

            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.clock.tick(60)
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.0f}')

if __name__ == '__main__':
    app = App()
    app.run()