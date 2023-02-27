import pygame
from settings import *
# for animation
from collections import deque

class Bird(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites_group)
        self.game = game
        self.image = game.bird_images[0]
        self.rect = self.image.get_rect(center=BIRD_POS)
        # self image as mask
        # self.mask = pygame.mask.from_surface(self.image)
        # mask from file
        self.mask = pygame.mask.from_surface(game.mask_image)

        # animation
        self.images = deque(game.bird_images)
        self.animation_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.animation_event, BIRD_ANIMATION_TIME)

        # 04 Gravity
        self.falling_velocity = 0
        self.first_jump = False
        # bird jump angle
        self.angle = 0

    def animate(self):
        # play order forward 1 or backward -1
        self.images.rotate(1)
        self.image = self.images[0]

    def use_gravity(self):
        if self.first_jump:
            self.falling_velocity += GRAVITY
            self.rect.y += self.falling_velocity + 0.5 * GRAVITY

    def jump(self):
        self.first_jump = True
        self.falling_velocity = BIRD_JUMP
        self.game.sound.wing_sound.play()

    def rotate(self):
        if self.first_jump:
            if self.falling_velocity < -BIRD_JUMP:
                self.angle = BIRD_JUMP_ANGLE
            else:
                self.angle = max(-2.5 * self.falling_velocity, -90) % 359
            self.image = pygame.transform.rotozoom(self.image, self.angle, 1)
            # rotate file mask
            mask_image = pygame.transform.rotozoom(self.game.mask_image, self.angle, 1)
            self.mask = pygame.mask.from_surface(mask_image)

    def check_collision(self):
        # center of each iterarion, this is worst
        # pos = self.rect.center
        # self.rect = self.image.get_rect(center= pos)

        # Mask collision, # self image as mask
        # self.mask = pygame.mask.from_surface(self.image)

        hit = pygame.sprite.spritecollide(self, self.game.pipe_group, dokill=False, collided=pygame.sprite.collide_mask)
        if hit or self.rect.bottom > GROUND_Y or self.rect.top < -self.image.get_height():
            self.game.sound.hit_sound.play() # 07
            pygame.time.wait(1000)
            self.game.new_game()

    def update(self):
        self.use_gravity()
        self.check_collision() # 05

    def check_event(self, event):
        if event.type == self.animation_event:
            self.animate()
            self.rotate()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.jump()
