import pyray, pathlib
from raylib import MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT
from raylib.colors import *
from settings import *
from random import randrange

# movement of images =================================== {#8fa, 0}
class SpriteUnit:
    def __init__(self, handler, x, y):
        
        self.handler = handler
        self.x, self.y = x, y
        # load images
        self.image_index = randrange(len(handler.images))
        self.image = handler.images[self.image_index]
        self.x, self.y = x, y
        self.angle = 0
        self.rotation_speed = self.get_speed()
        self.speed_x, self.speed_y = self.get_speed(), self.get_speed()
        self.center = self.image.width * 0.5, self.image.height * 0.5
        
    def get_speed(self):
        return randrange(-SPEED, SPEED)

    # movement and bound collision
    def translate(self):
        self.x += self.speed_x * self.handler.app.dt
        self.y += self.speed_y * self.handler.app.dt
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.speed_x *= -1
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.speed_y *= -1
    
    # rotation
    def rotate(self):
        self.angle += self.rotation_speed * self.handler.app.dt
 
    def update(self):
        self.rotate()
        self.translate()

    def draw(self):
        pyray.draw_texture_pro(self.image,
            (0, 0, self.image.width, self.image.height),
            (self.x, self.y, self.image.width, self.image.height),
            self.center, self.angle, WHITE)


# load image and set group ==================================={#2fa, 0}
class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.load_images()
        self.sprites = [SpriteUnit(self, WINDOW_WIDTH//2,WINDOW_HEIGHT//2 )]

    def add_sprite(self, x, y):
        for i in range(NUM_SPRITES_PER_CLICK):
            self.sprites.append(SpriteUnit(self, x, y))

    def del_sprites(self):
        for i in range(NUM_SPRITES_PER_CLICK):
            if len(self.sprites):
                self.sprites.pop()
                
    def load_images(self):
        paths = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        return [pyray.load_texture(str(path)) for path in paths]

    def update(self):
        self.on_mouse_pressed()
        [sprite.update() for sprite in self.sprites]

    def draw(self):
        [sprite.draw() for sprite in self.sprites]

    def on_mouse_pressed(self):
        if pyray.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
            pos = pyray.get_mouse_position()
            self.add_sprite(pos.x, pos.y)
        elif pyray.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT):
            self.del_sprites()


# main class =============================================={#cfa, 0}
class App:
    def __init__(self):
        
        pyray.init_window(*RES, 'Raylib GPU test') 
        self.sprite_handler = SpriteHandler(self)        
        self.dt = 0.0

    def draw_fps(self):
        text = f'{pyray.get_fps():.0f} FPS | {len(self.sprite_handler.sprites)} SPRITES'.center(22, ' ')
        pyray.draw_rectangle(10, 0, 30 * int(len(text) * 0.6), 30, BLACK)
        pyray.draw_text(text, 20, 0, 30, GREEN)

    def update(self):
        self.dt = pyray.get_frame_time()
        self.sprite_handler.update()

    def draw(self):      
        pyray.begin_drawing()
        pyray.clear_background(BLACK)
        self.sprite_handler.draw()
        self.draw_fps()
        pyray.end_drawing()

    def run(self):
        while not pyray.window_should_close():
            self.update()            
            self.draw()
        self.destroy()

    def destroy(self):
        [pyray.unload_texture(tex) for tex in self.sprite_handler.images]
        pyray.close_window()

if __name__ == '__main__':
    app = App()
    app.run()
                      
            








