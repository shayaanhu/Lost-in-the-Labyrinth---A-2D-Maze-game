
import pygame
from random import choice

# Resolution for the game (pixels)
Width = 800
Height = 600
Resolution = Width, Height

# Forming the grid for the game
Tile = 100
Rows = Width // Tile
Columns = Width // Tile

# Creating a class for the cells in the maze grid
class Cell:
    def __init__(self, x, y):                                                    # x and y are coordinates of the cell
        self.x, self.y = x, y                                                    # attributing the cordinates to the cell
        self.walls = {"Top": True, "Right": True, "Left": True, "Bottom": True}  # this indicates whether or not there is a wall in that direction
        self.visited = False                                                     # originally cell is not visited
    def draw_current_cell(self): # display where the current cell is
      x,y=self.x * Tile,self.y * Tile
      pygame.draw.rect(sc,pygame.Color('saddlebrown'),(x+2,y+2,Tile-2,Tile-2))#paint current cell with a different color
    def draw(self):
        x, y = self.x * Tile, self.y * Tile
        if self.visited:
            pygame.draw.rect(sc, pygame.Color("black"), (x, y, Tile, Tile))    # if cell visited, color it black

        # creating lines according to the starting coordinate
        if self.walls["Top"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y), (x + Tile, y), 2)

        if self.walls["Right"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x + Tile, y), (x + Tile, y + Tile), 2)

        if self.walls["Left"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y + Tile), (x, y), 2)

        if self.walls["Right"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x + Tile, y + Tile), (x, y + Tile), 2)

    def check_cell(self,x,y): #checking a cell by its coordinates 
      find_index=lambda x,y:x+y * Columns #formula to find index since they are stored in a 1D form in a list
      if x<0 or x>Columns-1 or y<0 or y>Rows-1: #if the cell snt beyond the edges of the field/maze
        return False
      return grid_cells[find_index(x,y)]
    
    def check_neighbors(self):
      neighbors=[]
      top=self.check_cell(self.x,self.y-1)
      right=self.check_cell(self.x+1,self.y)
      bottom=self.check_cell(self.x,self.y+1)
      left=self.check_cell(self.x-1,self.y)
      #if these neighbors arent beyond the boundary and havent been visited, put them in list(to visit)
      if top and not top.visited:
        neighbors.append(top)
      if right and not right.visited:
        neighbors.append(right)
      if bottom and not bottom.visited:
        neighbors.append(bottom)
      if left and not left.visited:
        neighbors.append(left)
      return choice(neighbors) if neighbors else False
    
def remove_walls(current,next): #doesnt change anything just changes the attributed of the walls so a cell isnt completly blocked from all four ends.
  dx=current.x - next.x
  if dx==1:
    current.walls['Left']=False
    next.walls['Right']=False
  elif dx==-1:
    
    current.walls['Right']=False
    next.walls['Left']=False
  dy=current.y-next.y
  
  if dy==1:
    current.walls['Top']=False
    next.walls['Bottom']=False
  elif dy==-1:
    
    current.walls['Bottom']=False
    next.walls['Top']=False

grid_cells = [Cell(col, row) for row in range(Rows) for col in range(Columns)]
current_cell = grid_cells[0]
stack = []

# Creating the UI
pygame.init()
sc = pygame.display.set_mode(Resolution)
clock = pygame.time.Clock()

while True:
    sc.fill(pygame.Color("aquamarine4"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid_cells]
    current_cell.visited=True #mark the current cell as visited to avoid going back there later
    current_cell.draw_current_cell()
    next_cell=current_cell.check_neighbors()
    if next_cell:
      next_cell.visited=True
      stack.append(current_cell)
      remove_walls(current_cell,next_cell)
      current_cell=next_cell
    elif stack:
      current_cell= stack.pop()
    pygame.display.flip()
    clock.tick(30)







