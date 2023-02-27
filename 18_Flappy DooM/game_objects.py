import pygame
from settings import *

class Background:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.speed = SCROLL_SPEED / 2
        self.image = self.game.background_image

    def update(self):
        self.x = (self.x - self.speed * self.game.dt) % -WINDOW_WIDTH

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        self.game.screen.blit(self.image, (WINDOW_WIDTH + self.x, self.y))

class Ground(Background):
    def __init__(self, game):
        super().__init__(game)
        self.y = GROUND_Y
        self.speed = SCROLL_SPEED + 50
        self.image = self.game.ground_image

class Sound:
    def __init__(self):
        self.hit_sound = pygame.mixer.Sound('sound/hit.wav')
        self.point_sound = pygame.mixer.Sound('sound/point.wav')
        self.wing_sound = pygame.mixer.Sound('sound/wing.wav')
        self.music = pygame.mixer.Sound('sound/theme.mp3')

class Score:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('font/doom.ttf', 100)
        self.font_pos = WINDOW_WIDTH//2, WINDOW_HEIGHT//8

    def draw(self):
        score = self.game.pipe_handler.passed_pipes
        self.text = self.font.render(f'{score}', True, 'red')
        self.game.screen.blit(self.text, self.font_pos)