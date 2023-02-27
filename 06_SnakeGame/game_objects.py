import pygame as pg  
from random import randrange

vec2 = pg.math.Vector2

class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        # snake
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE -2, game.TILE_SIZE -2])
        # center of the snake square
        self.rect.center = self.get_random_position()
        # for move
        self.direction = vec2(0, 0)
        self.step_delay = 500 # miliseconds
        # to add delay to movement
        self.time = 0
        self.length = 1
        # to grow snake
        self.segments = []
        # dictionary of booleans to disable a specified key when other is pressed
        self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1,}

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and self.directions[pg.K_UP]:
                self.direction = vec2(0, -self.size)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1,}
            if event.key == pg.K_DOWN and self.directions[pg.K_DOWN]:
                self.direction = vec2(0, self.size)
                self.directions = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1,}
            if event.key == pg.K_LEFT and self.directions[pg.K_LEFT]:
                self.direction = vec2(-self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0,}
            if event.key == pg.K_RIGHT and self.directions[pg.K_RIGHT]:
                self.direction = vec2(self.size, 0)
                self.directions = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1,}

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            return True
        return False

    # random position for the center of squares
    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE - self.size // 2, self.size)] * 2

# if sneke cross the borders, create a new game and restart
    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE:
            self.game.new_game()
        if self.rect.top < 0 or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

# compare the position of the snake and food and change to random if they are equals
    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            # increase when eats food
            self.length += 1
            self.step_delay /= 1.05

# check at each step of the segments using the coordinates of the segments
# when the snake traspase itsef the length of segments always is diferent then new game
    def checK_selfeating(self):
        if len(self.segments) != len(set(segment.center for segment in self.segments)):
            self.game.new_game()

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            # add a square to the next position
            self.segments.append(self.rect.copy())
            # slice the list along the length of the snake
            self.segments = self.segments[-self.length:]

    def update(self):
        self.checK_selfeating()
        self.check_borders()
        self.check_food()
        self.move()

# display each segment separately
    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]

class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.rect.Rect([0, 0, game.TILE_SIZE -2, game.TILE_SIZE -2])
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'orange', self.rect)