import pygame, sys
from datetime import datetime

pygame.init()
clock = pygame.time.Clock()
RES = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(RES, vsync=1)

# Game Setup
font = pygame.font.SysFont('Verdana', 100)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update ====================================
    screen.fill('blue')

    # get time
    t = datetime.now()
    # draw clock
    time_render = font.render(f'{t:%H:%M:%S}', True, 'green4', 'darkorange')
    screen.blit(time_render, (10,10))

    pygame.display.update()
    clock.tick(60)
