# Creation Order
# 01 Bird | 02 Background | 03 Ground | 04 Gravity | 05 Collisions
# 07 Sound | 08 pipes

import pygame, sys, time
from settings import *
from bird import Bird
from game_objects import *
from pipe import *
from doom_fire import*

class FlappyDoom:
    def __init__(self):
        pygame.init()
        self.p_time = time.time()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        # game setup
        self.load_assets()
        self.new_game()
        # sound
        self.sound = Sound()
        # score
        self.score = Score(self)

        self.sound.music.play() # play music game

    def load_assets(self):
        # 01 bird
        self.bird_images = [pygame.image.load(f'graphics/bird/{i}.png').convert_alpha() for i in range(5)]
        self.bird_images = [pygame.transform.rotozoom(sprite, 0, BIRD_SCALE) for sprite in self.bird_images]
        # bird mask
        mask_image = pygame.image.load('graphics/bird/mask.png').convert_alpha()
        self.mask_image = pygame.transform.rotozoom(mask_image, 0, BIRD_SCALE)


        # 02 Background
        self.background_image = pygame.image.load('graphics/level/bg.png').convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, RES)

        # 03 Ground
        self.ground_image = pygame.image.load('graphics/level/ground.png').convert()
        self.ground_image = pygame.transform.scale(self.ground_image, (WINDOW_WIDTH, GROUND_HEIGHT))

        # 08 pipes
        self.top_pipe_image = pygame.image.load('graphics/level/top_pipe.png')
        self.top_pipe_image = pygame.transform.scale(self.top_pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.bottom_pipe_image = pygame.transform.flip(self.top_pipe_image, False, True)

    def new_game(self):
        self.all_sprites_group = pygame.sprite.Group()
        self.bird = Bird(self) # 01
        self.background = Background(self) # 02
        self.ground = Ground(self) # 03
        self.pipe_group = pygame.sprite.Group() # collision
        self.pipe_handler = PipeHandler(self)
        
        self.doom_fire = Doom_fire(self)

    def draw(self):
        # self.screen.fill('black')
        # game setup -----------------------------------
        self.background.draw()
        self.doom_fire.draw() # ---
        self.all_sprites_group.draw(self.screen)
        self.ground.draw()
        self.score.draw()
        # debug ------------------------------
        # pygame.draw.rect(self.screen, 'green', self.bird.rect, 2)
        # self image as mask
        # self.bird.mask.to_surface(self.screen, unsetcolor=None, dest=self.bird.rect, setcolor='yellow')

    def update(self):
        pygame.display.update()
        self.clock.tick(60)
        pygame.display.set_caption(f'{self.clock.get_fps():.0f}')
        # game setup ----------------------------------
        self.all_sprites_group.update()
        self.background.update()
        self.ground.update()
        self.pipe_handler.update()
        
        self.doom_fire.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # User events -----------------------------
            self.bird.check_event(event)

    def run(self):
        while True:
            self.dt = time.time() - self.p_time
            self.p_time = time.time()
            if self.dt > 0.05: continue

            self.check_events()
            self.draw()
            self.update()

if __name__ == '__main__':
    game = FlappyDoom()
    game.run()
