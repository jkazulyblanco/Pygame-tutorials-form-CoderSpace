import pygame, sys, math
from datetime import datetime

RES = WIDTH, HEIGHT = 700, 700
MID = HALF_W, HALF_H = WIDTH//2, HEIGHT//2
RADIUS = HALF_H -45
time_radius = {'sec': RADIUS -20, 'min': RADIUS -55, 'hour': RADIUS -100, 'digit': RADIUS - 30}

# Style
RADIUS_ARK = RADIUS + 8

def get_clock_pos(clock_dict, clock_hand, key):
    x = HALF_W + time_radius[key] * math.cos(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    y = HALF_W + time_radius[key] * math.sin(math.radians(clock_dict[clock_hand]) - math.pi / 2)
    return x, y

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(RES, vsync=1)

# Game Setup ============================================
font = pygame.font.SysFont('Verdana', 30)
back_img = pygame.image.load('img/bg4.jpg').convert()
background = pygame.image.load('img/2.png').convert_alpha()
bg = pygame.transform.scale(background, (1050,700))
# For Animation
back_img_rect = back_img.get_rect(center= (WIDTH, HEIGHT)) # pivot
dx, dy = 1, 1 # direction

clock_12 = dict(zip(range(12), range(0, 360, 30))) # for hours
clock_60 = dict(zip(range(60), range(0, 360, 6))) # for min and sec


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update ====================================
    dx *= -1 if back_img_rect.left > 0 or back_img_rect.right < WIDTH else 1
    dy *= -1 if back_img_rect.top > 0 or back_img_rect.bottom < HEIGHT else 1
    back_img_rect.centerx += dx
    back_img_rect.centery += dy
    
    screen.blit(back_img, back_img_rect)
    screen.blit(bg, (-174,0))

    # get time
    t = datetime.now()
    hour, minute, second = ((t.hour%12) * 5 + t.minute //12) %60, t.minute, t.second
    # pygame.draw.circle(screen, 'darkgrey', MID, RADIUS )

    # draw Analog clock
    # base
    for digit, pos in clock_60.items():
        radius = 20 if not digit%3 and not digit%5 else 8 if not digit%5 else 2
        pygame.draw.circle(screen, 'cyan3', get_clock_pos(clock_60, digit, 'digit'), radius, 7)
    # line seconds
    pygame.draw.line(screen, 'red3', MID, get_clock_pos(clock_60, hour, 'hour'), 14)
    pygame.draw.line(screen, 'blue2', MID, get_clock_pos(clock_60, minute, 'min'), 7)
    pygame.draw.line(screen, 'green3', MID, get_clock_pos(clock_60, second, 'sec'), 4)
    pygame.draw.circle(screen, 'cyan', MID, 8 )

    # draw Digital clock
    time_render = font.render(f'{t:%H:%M:%S}', True, 'green')
    screen.blit(time_render, (0,0))

    # draw arc
    sec_angle = -math.radians(clock_60[t.second]) + math.pi /2
    pygame.draw.arc(screen, 'cyan',
        (HALF_W-RADIUS_ARK, HALF_H-RADIUS_ARK, 2*RADIUS_ARK, 2*RADIUS_ARK),
        math.pi/2, sec_angle, 8)


    pygame.display.update()
    clock.tick(30)
