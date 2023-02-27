'''
Iterative Implementation of Backtracking (DFS)

1. Choose the inital cell, mark it as visited and push it to the stack
2. while th stack is not empty
    1. Pop a cell from the stack and make it a current cell
    2. If the curren cell has any neighbours which have not been visited
        1. Push the curent cell to the stack
        2. Choose one of the unvisited neghbours
        3. Remove the wall between the current cell and the chosen cell
        4. Mark the chosen cell as visited and push it to the stack
'''

import pygame, sys 
from random import choice

RES = WIDTH, HEIGHT = 1200, 700
TILE = 50
cols, rows = WIDTH//TILE, HEIGHT//TILE

class Cell:
    def __init__(self, x, y):
        self.x, self.y, = x, y
        self.walls = {'top':True, 'right':True, 'bottom':True, 'left':True}
        self.visited = False

    def draw_current_cell(self):
        x, y, = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, 'magenta4', (x+5, y+5, TILE-10, TILE-10), 0, 16)

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        # if the cell is visited "paint in black"
        if self.visited:
            pygame.draw.rect(screen, 'gray17', (x,y,TILE,TILE))
        # draw lines of the maze
        if self.walls['top']:
            pygame.draw.line(screen, 'orange', (x,y), (x+TILE, y) , 2)
        if self.walls['right']:
            pygame.draw.line(screen, 'orange', (x+TILE, y), (x+TILE, y+TILE) , 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, 'orange', (x+TILE, y+TILE), (x, y+TILE) , 2)
        if self.walls['left']:
            pygame.draw.line(screen, 'orange', (x, y+TILE), (x, y), 2)

    def check_cell(self, x, y):
        # index = x + y * cols
        find_index = lambda x, y: x + y * cols
        # if check cell is in the limit
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x,y)]

    def check_neighbors(self):
        neighbors = []
        # to visit
        top = self.check_cell(self.x, self.y -1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False

# change some values in walls dict
def remove_walls(current, naxt):
    dx = current.x - naxt.x
    if dx == 1:
        current.walls['left'] = False
        naxt.walls['right'] =  False
    elif dx == -1:
        current.walls['right'] = False
        naxt.walls['left'] = False

    dy = current.y - naxt.y
    if dy == 1:
        current.walls['top'] = False
        naxt.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        naxt.walls['top'] = False
        

# ==============================================
pygame.init() 
screen = pygame.display.set_mode(RES, vsync=1)
clock = pygame.time.Clock()

# Game setup ========================================
# instance in array x y
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

current_cell = grid_cells[0]
stack = []

colors, color = [], 40 # 01


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw - Update
    screen.fill('darkslategray')

    # Cells and current cell
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    # 01
    [pygame.draw.rect(screen, colors[i],
    (cell.x*TILE+5, cell.y*TILE+5, TILE-10, TILE-10),
    border_radius=12) for i, cell in enumerate(stack)]


    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        # remove walls between cells
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.update()
    clock.tick(60)