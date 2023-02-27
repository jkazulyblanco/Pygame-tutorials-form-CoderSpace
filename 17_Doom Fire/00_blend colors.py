import pygame, sys

RES = WIDTH, HEIGHT = 1280, 720

LERP_COLORS = 4
COLORS = ['black','red','orange','yellow','white']

class Doom_fire:
    def __init__(self, app):
        self.app = app
        self.palette = self.get_palette()

    # Blend colors 
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

    def update(self):...

    def draw(self):
        self.draw_palette()


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
        self.screen.fill('gray15')
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

