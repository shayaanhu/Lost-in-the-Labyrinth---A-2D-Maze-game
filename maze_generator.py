import pygame
from random import choice, randrange

# Set up the screen dimensions and tile size
RES = WIDTH, HEIGHT = 900, 600
TILE = 100

# Calculate the number of columns and rows based on the screen dimensions and tile size
cols, rows = WIDTH // TILE, HEIGHT // TILE

class Cell:
    def __init__(self, x, y):
        # Store the x and y position of the cell in the grid
        self.x, self.y = x, y
        
        # Define the walls of the cell as True initially (meaning they exist)
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # Keep track of whether the cell has been visited during maze generation
        self.visited = False
        
        # Set the thickness of the walls (for drawing purposes later on)
        self.thickness = 4

        # For Dijkstra implementation
        self.paths = {}
        

    def draw(self, sc):
        # Calculate the x and y pixel positions of the cell on the screen
        x, y = self.x * TILE, self.y * TILE

        # Draw the top wall if it exists
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), self.thickness)
            
        # Draw the right wall if it exists
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
            
        # Draw the bottom wall if it exists
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y + TILE), (x , y + TILE), self.thickness)
            
        # Draw the left wall if it exists
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x, y), self.thickness)


    def get_rects(self):
        rects = []
        
        # Calculate the x and y pixel positions of the cell on the screen
        x, y = self.x * TILE, self.y * TILE
        
        # If the top wall exists, create a rectangle for it and append it to the list
        if self.walls['top']:
            rects.append(pygame.Rect( (x, y), (TILE, self.thickness) ))
        
        # If the right wall exists, create a rectangle for it and append it to the list
        if self.walls['right']:
            rects.append(pygame.Rect( (x + TILE, y), (self.thickness, TILE) ))
        
        # If the bottom wall exists, create a rectangle for it and append it to the list
        if self.walls['bottom']:
            rects.append(pygame.Rect( (x, y + TILE), (TILE , self.thickness) ))
        
        # If the left wall exists, create a rectangle for it and append it to the list
        if self.walls['left']:
            rects.append(pygame.Rect( (x, y), (self.thickness, TILE) ))
        
        # Return the list of wall rectangles
        return rects


    def check_cell(self, x, y):
        # Define a lambda function to find the index of a cell in the grid_cells list
        find_index = lambda x, y: x + y * cols
        
        # If the given x or y coordinate is out of bounds, return False
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        
        # Otherwise, return the cell at the given x, y coordinates using the find_index function
        return self.grid_cells[find_index(x, y)]


    def check_neighbors(self, grid_cells):
        # Set the grid_cells attribute to the provided grid_cells list
        self.grid_cells = grid_cells
        
        # Initialize an empty list to hold the unvisited neighbors of the cell
        neighbors = []
        
        # Check the cells to the top, right, bottom, and left of the current cell, and add any unvisited cells to the neighbors list

        top = self.check_cell(self.x, self.y - 1)
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
        
        # If there are any unvisited neighbors, return a randomly chosen neighbor.
        # Otherwise, return False to indicate that there are no unvisited neighbors.
        return choice(neighbors) if neighbors else False


def remove_walls(current, next):

    # dx = horizontal distance between the x coordinates of the two cells
    dx = current.x - next.x

    # When dx == 1, current is on right of next. We remove left wall of current and right wall of next.
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False

    # When dx == -1, current is on left of next. We remove right wall of current and left wall of next.
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False

    # dy = vertical distance between the y coordinates of the two cells
    dy = current.y - next.y

    # When dy == 1, current is on top of next. We remove top wall of current and bottom wall of next.
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False

    # When dy == -1, current is below next. We remove bottom wall of current and top wall of next.
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

def generate_maze():

    # Initializing the grid
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

    # Current cell is set to top left cell
    current_cell = grid_cells[0]

    array = [] # to keep track of visited cells
    break_count = 1 # to check if all cells are visited (to stop the generation)

    while break_count != len(grid_cells):

        current_cell.visited = True
        next_cell = current_cell.check_neighbors(grid_cells) # next cell = random unvisited neighbor

        if next_cell:
            next_cell.visited = True
            break_count += 1
            array.append(current_cell)
            remove_walls(current_cell, next_cell) # removing walls to generate the maze
            current_cell = next_cell

        elif array:
            current_cell = array.pop() # if there is no next cell, we use DFS to backtrack

    return grid_cells # returning the final maze