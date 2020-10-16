import pygame
import math
from queue import PriorityQueue


# sets up the display
DISPLAY_WIDTH = 800
DISPLAY_WINDOW = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_PINK = (255, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (104, 120, 143)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = COLOR_WHITE
        self.neighbors = []

    # gets the position of the Node on our grid
    def get_pos(self):
        return self.row, self.col

    # color is green if the Node is open
    def is_open(self):
        return self.color == COLOR_GREEN

    # color is red if the Node is closed
    def is_closed(self):
        return self.color == COLOR_RED

    # color is black if the Node is a barrier
    def is_barrier(self):
        return self.color == COLOR_BLACK

    # color is blue if the Node is the starting point
    def is_start(self):
        return self.color == COLOR_BLUE

    # color is pink if the Node is the ending point
    def is_end(self):
        return self.color == COLOR_PINK

    # board is reset to white
    def reset(self):
        self.color = COLOR_WHITE

    # all of our make functions to make a Node a certain color

    def make_open(self):
        self.color = COLOR_GREEN

    def make_closed(self):
        self.color = COLOR_RED

    def make_barrier(self):
        self.color = COLOR_BLACK

    def make_start(self):
        self.color = COLOR_BLUE

    def make_end(self):
        self.color = COLOR_PINK

    def make_path(self):
        self.color = COLOR_CYAN

    # draw function using pygame to draw a rectangle on the screen
    # width is passed is twice becuase it is a square (has the same x and y)
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Goes down a row if it is not a barrier
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        # Goes up a row if it is not a barrier
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Goes right a row if it is not a barrier
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Goes left a row if it is not a barrier
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# this function will calculate our h cost
# h cost = distance from start point to the end point
# the formula to calculate distance is manhattan
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# draws the shortest path
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# A* (star) algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
    
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False

# sets up the grid in a 2d array
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for y in range(rows):
            node = Node(i, y, gap, rows)
            grid[i].append(node)

    return grid

# draws the grid lines
def draw_grid(window, rows, width):
    gap = width // rows

    # draws the vertical and horizontal lines
    for i in range(rows):
        pygame.draw.line(window, COLOR_GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, COLOR_GREY, (i * gap, 0), (i * gap, width))

# draws the current state of the program
def draw(window, grid, rows, width):
    window.fill(COLOR_WHITE)

    # loops through our 2d array and draws all of the Node colors
    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()

# takes the cursor position and gives the Node that is clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    # continously checks for events happening within our program
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            # right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # lambda is an anon function
                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(DISPLAY_WINDOW, DISPLAY_WIDTH)