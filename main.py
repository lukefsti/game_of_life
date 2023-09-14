import os
import numpy as np
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 700
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Enhanced Game of Life")

grid = np.zeros((ROWS, COLS))

font = pygame.font.SysFont('Arial', 30)

def draw_status():
    if paused:
        label = font.render("PAUSED", True, RED)
    else:
        label = font.render("RUNNING", True, GREEN)
    screen.blit(label, (10, 10))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_cells():
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == 1:
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def update():
    global grid
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            state = grid[row][col]
            neighbors = np.sum(grid[max(row - 1, 0):min(row + 2, ROWS), max(col - 1, 0):min(col + 2, COLS)]) - state
            if state == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row][col] = 0
            elif state == 0 and neighbors == 3:
                new_grid[row][col] = 1
    grid = new_grid

running = True
paused = False
clock = pygame.time.Clock()
speed = 10

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col, row = x // CELL_SIZE, y // CELL_SIZE
            grid[row][col] = 1 - grid[row][col]  # Toggle cell
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                speed += 5
            elif event.key == pygame.K_DOWN:
                speed = max(5, speed - 5)

    draw_cells()
    draw_grid()
    draw_status()

    if not paused:
        update()

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
