import pygame, random
from settings import *

class PipeHandler:
    def __init__(self, game):
        self.game = game
        self.pipe_distance = PIPES_GAP_X
        # counter of pipes
        self.pipes = []
        self.passed_pipes = 0

    def update(self):
        self.generate_pipes()
        self.count_passed_pipes()

    @staticmethod
    def get_gap_y_position():
        return random.randint(PIPES_GAP_Y, WINDOW_HEIGHT - PIPES_GAP_Y)
    
    def generate_pipes(self):
        if self.game.bird.first_jump:
            self.pipe_distance += SCROLL_SPEED * self.game.dt
            if self.pipe_distance > PIPES_GAP_X:
                self.pipe_distance = 0
                gap_y = self.get_gap_y_position()

                TopPipe(self.game, gap_y)
                pipe = BottomPipe(self.game, gap_y)
                self.pipes.append(pipe) # counter of pipes

    def count_passed_pipes(self):
        for pipe in self.pipes:
            if BIRD_POS[0] > pipe.rect.right:
                self.game.sound.point_sound.play()
                self.passed_pipes += 1
                # remove innesesary pipes from list
                self.pipes.remove(pipe) 

class TopPipe(pygame.sprite.Sprite):
    def __init__(self, game, gapY_pos):
        super().__init__(game.pipe_group, game.all_sprites_group)
        self.game = game
        self.image = game.top_pipe_image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = WINDOW_WIDTH, gapY_pos - HALF_GAP_Y - GROUND_HEIGHT
        # self image as mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.left -= SCROLL_SPEED * self.game.dt
        if self.rect.right < 0:
            self.kill()

class BottomPipe(TopPipe):
    def __init__(self, game, gapY_pos):
        super().__init__(game, gapY_pos)
        # self.game = game
        self.image = game.bottom_pipe_image
        self.rect.topleft = WINDOW_WIDTH, gapY_pos + HALF_GAP_Y - GROUND_HEIGHT
