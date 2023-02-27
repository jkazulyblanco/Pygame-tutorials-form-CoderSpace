import pygame, sys, time
from random import randrange, uniform
import pygame.freetype as ftype # text method
from settings import *

# movement of images =================================== {#8fa, 0}
class SpriteUnit(pygame.sprite.Sprite):
    def __init__(self, handler, x, y):
        super().__init__(handler.group)
        self.handler = handler
        self.x, self.y = x, y
        # load images
        self.image_index = randrange(len(handler.images))
        self.image = handler.images[self.image_index]
        self.rect = self.image.get_rect()
        # movement
        self.speed_x, self.speed_y = self.get_speed(), self.get_speed()
        # rotation
        self.angle = 0
        self.rotation_speed = self.get_speed()

    # rotation
    def rotate(self):
        self.angle += self.rotation_speed * self.handler.app.dt
        # self.image = pygame.transform.rotate(self.handler.images[self.image_index], self.angle)
        self.image = self.handler.rot_cache[self.image_index][int(NUM_ANGLES * (self.angle %360) /360)]
        self.rect = self.image.get_rect()

    # movement and bound collision
    def translate(self):
        self.x += self.speed_x * self.handler.app.dt
        self.y += self.speed_y * self.handler.app.dt
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.speed_x *= -1
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.speed_y *= -1

    def get_speed(self):
        return randrange(-SPEED, SPEED)
    
    def update(self):
        self.translate()
        self.rotate()
        self.rect.center = self.x, self.y


# load image and set group ==================================={#2fa, 0}
class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.load_images()
        self.group = pygame.sprite.Group()
        # 02 rotation Cache
        self.rot_cache = self.get_rot_cache()

        self.sprites = [SpriteUnit(self, WINDOW_WIDTH/2,WINDOW_HEIGHT/2 )]

        # 02 rotation Cache
    def get_rot_cache(self):
        rot_cache = {}
        for index, image in enumerate(self.images):
            rot_cache[index] = []
            for angle in range(NUM_ANGLES):
                rot_image = pygame.transform.rotate(image, angle * 360 / NUM_ANGLES)
                rot_cache[index].append(rot_image)
        return rot_cache                

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
        atlas = pygame.image.load('among us.png').convert_alpha()
        custom_quads = []
        for y in range(4):
            for x in range(3):
                x_offset = 375*x
                y_offset = 377*y       
                character = quads_area(atlas, 123+x_offset, 51+y_offset, 258, 305)
                character = pygame.transform.scale(character, (64,70))
                custom_quads.append(character)
        return custom_quads

    def update(self):
        self.group.update()

    def draw(self):
        self.group.draw(self.app.screen)


# main class =============================================={#cfa, 0}
class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.ptime = time.time()
        self.screen = pygame.display.set_mode(RES)
        self.font = ftype.SysFont('Verdana', 30) # text method 
        
        self.sprite_handler = SpriteHandler(self)        
    
    def update(self):
        
        self.sprite_handler.update()
        
        # pygame setup ---------
        pygame.display.update()
        self.clock.tick(0)


    def draw(self):      
        self.screen.fill('gray14')
        self.sprite_handler.draw()

        # self.screen.blit(custom_quads[10], (100, 50))

        # text method {#2dc, 2}
        fps = f'{self.clock.get_fps():.0f} FPS | {len(self.sprite_handler.sprites)} SPRITES'
        self.font.render_to(self.screen, (10,10), text=fps, fgcolor='green', bgcolor='black')



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
                      
            








