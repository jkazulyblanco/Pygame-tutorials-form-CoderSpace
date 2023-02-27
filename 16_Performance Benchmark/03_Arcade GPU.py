import arcade, pathlib
from settings import *
from random import randrange

# movement of images =================================== {#8fa, 0}
class SpriteUnit(arcade.Sprite):
    def __init__(self, handler, x, y):
        self.handler = handler
        self.x, self.y = x, y
        super().__init__()
        
        self.image_index = randrange(len(handler.images))
        self.texture = handler.images[self.image_index]
        self.angle = 0
        self.rotation_speed = self.get_speed()
        self.speed_x, self.speed_y = self.get_speed(), self.get_speed()
        
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
        self.center_x, self.center_y = self.x, self.y


# load image and set group ==================================={#2fa, 0}
class SpriteHandler:
    def __init__(self, app):
        self.app = app
        self.images = self.load_images()
        self.sprites = arcade.SpriteList(use_spatial_hash=False)
        self.sprites.append(SpriteUnit(self, WINDOW_WIDTH//2,WINDOW_HEIGHT//2))
                     
    def add_sprite(self, x, y):
        for i in range(NUM_SPRITES_PER_CLICK):
            self.sprites.append(SpriteUnit(self, x, y))

    def del_sprite(self):
        for i in range(NUM_SPRITES_PER_CLICK):
            if len(self.sprites):
                self.sprites.pop()

    def load_images(self):
        paths = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        return [arcade.load_texture(str(path)) for path in paths]

    def update(self):
        self.sprites.update()

    def draw(self):
        self.sprites.draw()


# main class =============================================={#cfa, 0}
class App(arcade.Window):
    def __init__(self):
        super().__init__(*RES, center_window=True, antialiasing=False)
        self.dt = 0.0
        self.text = arcade.Text(text='text', start_x=0, start_y=WINDOW_HEIGHT - 30,
                        font_size=30, color=arcade.color.GREEN, bold=True)        
        self.sprite_handler = SpriteHandler(self)        
    
    def draw_fps(self):
        arcade.draw_xywh_rectangle_filled(self.text.x, self.text.y, *self.text.content_size,
                                        arcade.color.BLACK)
        self.text.text = f'{round(1/self.dt, 1)} FPS  |  {len(self.sprite_handler.sprites)}  SPRITES'
        self.text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.sprite_handler.add_sprite(x, y)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.sprite_handler.del_sprite()

    def on_update(self, delta_time):
        self.sprite_handler.update()
        self.dt = delta_time

    def on_draw(self):
        self.clear()
        self.sprite_handler.draw()
        self.draw_fps()

if __name__ == '__main__':
    app = App()
    app.run()
                      
            








