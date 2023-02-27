import pygame, sys, time, pathlib
from random import randrange
import pygame.freetype as ftype # text method
from settings import *
from pygame._sdl2.video import Window, Renderer, Texture, Image

# movement of images =================================== {#8fa, 0}
class SpriteUnit(pygame.sprite.Sprite):
    def __init__(self, handler, x, y):
        self.handler = handler
        super().__init__(handler.group)
        self.image_index = randrange(len(handler.images))
        self.image = Image(handler.images[self.image_index])
        self.x, self.y = x, y
        # load images
        self.rect = self.image.get_rect()
        self.orig_rect = self.rect.copy()
        # rotation
        self.angle = 0
        self.rotation_speed = randrange(-SPEED, SPEED)
        self.speed_x, self.speed_y = randrange(-SPEED, SPEED), randrange(-SPEED, SPEED)

    # rotation
    def rotate(self):
        self.angle += self.rotation_speed * self.handler.app.dt
        self.image.angle = self.angle
        self.rect.center = self.x, self.y

    # movement and bound collision
    def translate(self):
        self.x += self.speed_x * self.handler.app.dt
        self.y += self.speed_y * self.handler.app.dt
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.speed_x *= -1
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.speed_y *= -1
        self.rect.center = self.x, self.y
    
    def update(self):
        self.rotate()
        self.translate()


# load image and set group ==================================={#2fa, 0}
class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.load_images()
        self.group = pygame.sprite.Group()
        self.sprites = [SpriteUnit(self, WINDOW_WIDTH/2,WINDOW_HEIGHT/2 )]


    def on_mouse_pressed(self):
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0]:
            x, y = pygame.mouse.get_pos()
            self.add_sprite(x, y)
        elif mouse_button[2]:
            self.del_sprites()

    def add_sprite(self, x, y):
        for i in range(NUM_SPRITES_PER_CLICK):
            self.sprites.append(SpriteUnit(self, x, y))

    def del_sprites(self):
        for i in range(NUM_SPRITES_PER_CLICK):
            if len(self.sprites):
                sprite = self.sprites.pop()
                sprite.kill()

    def load_images(self):
        paths = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pygame.image.load(str(path)) for path in paths]
        return [Texture.from_surface(self.app.renderer, image) for image in images]

    def update(self):
        self.group.update()

    def draw(self):
        self.group.draw(self.app.renderer)


# main class =============================================={#cfa, 0}
class App:
    def __init__(self):
        pygame.init()
        self.window = Window(size=RES)
        self.renderer = Renderer(self.window)
        self.renderer.draw_color = (0,0,0, 1)
        self.clock = pygame.time.Clock()
        self.ptime = time.time()
        self.sprite_handler = SpriteHandler(self)        
        self.font = ftype.SysFont('Verdana', 30) # text method 
        self.fps_size = [30 * 13, 30 * 1.5]
        self.fps_surf = pygame.Surface(self.fps_size)
    
    def update(self):
        
        self.sprite_handler.update()
        
        self.clock.tick(0)


    def draw_fps(self):      
        self.fps_surf.fill('black')
        fps = f'{self.clock.get_fps():.0f} FPS | {len(self.sprite_handler.sprites)} SPRITES'
        self.font.render_to(self.fps_surf, (10,10), text=fps, fgcolor='green', bgcolor='black')
        tex = Texture.from_surface(self.renderer, self.fps_surf)
        tex.draw((0, 0, *self.fps_size), (0, 0, *self.fps_size))

    def draw(self):
        self.renderer.clear()
        self.sprite_handler.draw()
        self.draw_fps()
        self.renderer.present()

    def chek_events(self):
        # pygame setup
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.sprite_handler.on_mouse_pressed()

    def run(self):
        while True:
            # delta time
            self.dt = time.time() - self.ptime
            self.ptime = time.time()
            if self.dt > 0.05: continue


            self.chek_events()
            self.update()            
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
                      
