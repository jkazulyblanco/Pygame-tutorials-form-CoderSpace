import pygame, sys
from random import randrange as rnd

pygame.init()
clock = pygame.time.Clock()
window = WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode(window, vsync=1)

background = pygame.image.load('background.jpg').convert()
background.set_alpha(80) # trail effect
# paddle settings
paddle_w = 160
paddle_h = 20
paddle_speed = 15
paddle = pygame.Rect(WIDTH//2-paddle_w//2, HEIGHT-40, paddle_w, paddle_h)
# ball Settings
ball_radius = 15
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH-ball_rect), HEIGHT//2, ball_rect,ball_rect)
dx, dy = 1, -1
# block settings
block_list = [pygame.Rect(10+100*i, 10+40*j, 70,30) for i in range(10) for j in range(6)]
color_list = [(rnd(30,256), rnd(30,256), rnd(30,256)) for i in range(10) for j in range(6)]

def detect_collision(dx, dy, ball, rect):
    if dx > 0: delta_x = ball.right - rect.left
    else: delta_x = rect.right - ball.left
    
    if dy > 0: delta_y = ball.bottom - rect.top
    else: delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0,0))
    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(screen, 'blue', paddle, 0, 8)
    pygame.draw.circle(screen, 'grey', ball.center, ball_radius)
    
    # Update Ball
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    # collision left right
    if ball.centerx < ball_radius or ball.centerx > WIDTH-ball_radius:
        dx = -dx
    # collision top
    if ball.centery < ball_radius:
        dy = -dy
    # collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)
    # collision_blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
           
        # special effect
        hit_rect.inflate_ip(ball.width*2, ball.height*2)
        pygame.draw.rect(screen, hit_color, hit_rect)
        # fps += 2
    
    # Win, Game over
    # if ball.bottom > HEIGHT:
    #     print('GAME OVER')
    #     exit()
    # elif not len(block_list):
    #     print('YOU WIN')
    #     exit()


    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    pygame.display.update()
    clock.tick(60)