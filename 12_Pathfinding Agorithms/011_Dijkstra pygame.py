import pygame as pg
import sys
from heapq import *

def get_circle(x, y):
    return (x*TILE+TILE//2, y*TILE+TILE//2), TILE//4

def get_rect(x, y):
    return x*TILE+1, y*TILE+1, TILE-2, TILE-2

# Check neighbors
def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1,0], [0,-1], [1,0], [0,1]
    return [(grid[y+dy][x+dx], (x+dx, y+dy)) for dx, dy in ways if check_next_node(x+dx, y+dy)]

def heuristic(a, b):
    return abs(a[0] - b[0] + abs(a[1] - b[1]))

cols, rows = 23, 13
TILE = 50

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode([cols*TILE, rows*TILE], vsync=1)

# SURFACES ==============================================

# create grid
grid = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']
grid = [[int(char) for char in string] for string in grid]

# dict of adjacency list
graph = {} 
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x,y)] = graph.get((x,y), []) + get_next_nodes(x,y)

# BFS settings
start = (0,7)
goal = (22,7)           
queue = []
heappush(queue, (0, start))
cost_visited = {start: 0}
visited = {start: None}

bg = pg.image.load('graphics/2.png').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))


# Game Loop =============================================
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # Key events ====================================

    # Draw - Update =====================================
    # screen.fill('black')
    screen.blit(bg, (0,0))
    # BFS Work
    [pg.draw.rect(screen, 'darkgreen', get_rect(x,y), 1) for x, y in visited]
    [pg.draw.rect(screen, 'cyan4', get_rect(*xy)) for _, xy in queue]
    pg.draw.circle(screen, 'purple', *get_circle(*goal))

    # Dijkstra Logic
    if queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            queue = []
            continue

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    
    # Draw Path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.circle(screen, 'orangered3', *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(screen, 'slateblue', *get_circle(*start))
    pg.draw.circle(screen, 'magenta', *get_circle(*path_head))


    pg.display.update()
    clock.tick(20)
    pg.display.set_caption(f'fps: {clock.get_fps() :.0f}')

