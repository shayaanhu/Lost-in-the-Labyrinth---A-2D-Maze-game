import pygame, pip 
#import cv2
#import matplotlib.pyplot as plt
#import numpy as np
#from heapq import heappush, heappop
from maze_generator import * # import everything from maze_generator.py

class Food: 
    def __init__(self):
        self.img = pygame.image.load('C:/Users/shaya/Desktop/DSA Project - Maze Game - TEST/images/food.jpg').convert() # loading the image
        self.img = pygame.transform.scale(self.img, (TILE - 10, TILE - 10))                                                # scaling it down to fit in the grid cells
        self.rect = self.img.get_rect()                                                                                    # setting the rectangle attribute according to the dimensions of the maze
        self.set_pos()                                                                                                     # setting the initial position

    def set_pos(self):
        self.rect.topleft = randrange(cols) * TILE + 5, randrange(rows) * TILE + 5                                         # initializing the food at a random cell in the grid

    def draw(self):
        game_surface.blit(self.img, self.rect)                                                                             # drawing the food at that cell

# Function to check for collisions
def is_collide(x, y): 
    tmp_rect = player_rect.move(x, y)
    if tmp_rect.collidelist(walls_collide_list) == -1:
        return False
    return True

# Function to eat food, which makes the food disappear (and reappear at another random location) and increase the time by 3 seconds.
def eat_food():
    global time
    for food in food_list:
        if player_rect.collidepoint(food.rect.center):
            food.set_pos()
            time += 3
            return True
    return False

def dijkstra(graph, start, end):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    prev = {node: None for node in graph}
    heap = [(0, start)]
    while heap:
        (d, u) = heappop(heap)
        if u == end:
            break
        if d > dist[u]:
            continue
        for v, distance in graph[u]:
            alt = dist[u] + distance
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heappush(heap, (alt, v))
    path = []
    u = end
    while prev[u]:
        path.insert(0, u)
        u = prev[u]
    path.insert(0, start)
    return path

'''def display_path(path):
    if path!=None:
        for cell in path:
            x = cell
            y=cell
            pygame.draw.rect(screen, (0, 0, 255), (x * HEIGHT,y * WIDTH, HEIGHT, WIDTH))
            pygame.display.update()'''

def display_path(path):
    if path!=None:
        for cell in path:
            x, y = cell
            pygame.draw.rect(screen, (0, 0, 255), (x * HEIGHT, y * WIDTH, HEIGHT, WIDTH))
            pygame.display.update()

'''def display_path(path): #not working, displays the text instead 
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Path: {path}", True, (255, 255, 255))
    screen.blit(text, (10, 10))'''

# Checking if the game is over when time remaining is less than 0 seconds.
def is_game_over():
    global time, score, record, FPS, user_path
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        print(user_path)
        time, score, FPS = 30, 0, 60
        
        # Convert maze list into a graph dictionary
        maze_dict = {}
        for cell in maze:
            maze_dict[cell] = []
        graph = maze_dict

        # Call Dijkstra's algorithm with the graph dictionary
        start = maze[0]
        end = maze[-1]
        #pathway = dijkstra(graph, start, end)
        #display_path(pathway)
        
# To make it engaging, we built a best record system so players could track their progress at getting better at the game.
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
            return 0

# Function to keep track of the best record.
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

# UI
FPS = 60
pygame.init()
game_surface = pygame.Surface(RES)
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH + 300, HEIGHT))

# Background images
bg_game = pygame.image.load('C:/Users/shaya/Desktop/DSA Project - Maze Game - TEST/images/background.jpg').convert()
bg = pygame.image.load('C:/Users/shaya/Desktop/DSA Project - Maze Game - TEST/images/scoreboard.jpg').convert()

# Generating the maze
maze = generate_maze()

# Player settings
player_speed = 5
player_img = pygame.image.load('C:/Users/shaya/Desktop/DSA Project - Maze Game - TEST/images/player.png').convert() # loading the mouse image
player_img = pygame.transform.scale(player_img, (TILE - 2 * maze[0].thickness, TILE - 2 * maze[0].thickness))
player_rect = player_img.get_rect()
player_rect.center = TILE // 2, TILE // 2
directions = {'a': (-player_speed, 0), 'd': (player_speed, 0), 'w': (0, -player_speed), 's': (0, player_speed)} # setting the keyboard controls for WSAD
keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
direction = (0, 0)

# Food settings (number of food present in the maze)
food_list = [Food() for i in range(1)]

# Collision list
walls_collide_list = sum([cell.get_rects() for cell in maze], [])

# Timer, score and record
pygame.time.set_timer(pygame.USEREVENT, 1000)
time = 30
score = 0
record = get_record()

# Fonts
font = pygame.font.SysFont('Impact', 90)
text_font = pygame.font.SysFont('Impact', 50)

# Main loop for running the game:
while True:
    surface.blit(bg, (WIDTH, 0))
    surface.blit(game_surface, (0, 0))
    game_surface.blit(bg_game, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.USEREVENT:
            time -= 1

    # Controls and movement
    user_path=[]
    pressed_key = pygame.key.get_pressed()
    for key, key_value in keys.items():
        if pressed_key[key_value] and not is_collide(*directions[key]):
            user_path.append(pressed_key[key_value])
            direction = directions[key]
            break
    if not is_collide(*direction):
        player_rect.move_ip(direction)

    # Draw maze
    [cell.draw(game_surface) for cell in maze]

    # Gameplay
    if eat_food():
        FPS += 2
        score += 1
    is_game_over()

    # Draw player
    game_surface.blit(player_img, player_rect)

    # Draw food
    [food.draw() for food in food_list]

    # Draw scoreboard
    surface.blit(text_font.render('TIME', True, pygame.Color('cyan'), True), (WIDTH + 90, 30))
    surface.blit(font.render(f'{time}', True, pygame.Color('cyan')), (WIDTH + 90, 90))
    surface.blit(text_font.render('score:', True, pygame.Color('forestgreen'), True), (WIDTH + 70, 220))
    surface.blit(font.render(f'{score}', True, pygame.Color('forestgreen')), (WIDTH + 110, 280))
    surface.blit(text_font.render('record:', True, pygame.Color('magenta'), True), (WIDTH + 70, 400))
    surface.blit(font.render(f'{record}', True, pygame.Color('magenta')), (WIDTH + 110, 460))

    pygame.display.flip()
    clock.tick(FPS)
    
'''img = cv2.imread('maze.png') # read an image from a file using
cv2.circle(img,(5,220), 3, (255,0,0), -1) # add a circle at (5, 220)
cv2.circle(img, (25,5), 3, (0,0,255), -1) # add a circle at (5,5)
plt.figure(figsize=(7,7))
plt.imshow(img) # show the image
plt.show()    

class Vertex:
    def __init__(self,x_coord,y_coord):
        self.x=x_coord
        self.y=y_coord
        self.d=float('inf') #current distance from source node
        self.parent_x=None
        self.parent_y=None
        self.processed=False
        self.index_in_queue=None
def find_shortest_path(img,src,dst):
    pq=[] #min-heap priority queue
    imagerows,imagecols=img.shape[0],img.shape[1]
    matrix = np.full((imagerows, imagecols), None) 
    #access matrix elements by matrix[row][col]
    #fill matrix with vertices
    for r in range(imagerows):
        for c in range(imagecols):
            matrix[r][c]=Vertex(c,r)
            matrix[r][c].index_in_queue=len(pq)
            pq.append(matrix[r][c])
    #set source distance value to 0
    matrix[source_y][source_x].d=0
    #maintain min-heap invariant (minimum d Vertex at list index 0)
    pq = bubble_up(pq, matrix[source_y][source_x].index_in_queue)
#Implement euclidean squared distance formula
def get_distance(img,u,v):
    return 0.1 + (float(img[v][0])-float(img[u][0]))**2+(float(img[v][1])-float(img[u][1]))**2+(float(img[v][2])-float(img[u][2]))**2
#Return neighbor directly above, below, right, and left
def get_neighbors(mat,r,c):
    shape=mat.shape
    neighbors=[]
    #ensure neighbors are within image boundaries
    if r > 0 and not mat[r-1][c].processed:
         neighbors.append(mat[r-1][c])
    if r < shape[0] - 1 and not mat[r+1][c].processed:
            neighbors.append(mat[r+1][c])
    if c > 0 and not mat[r][c-1].processed:
        neighbors.append(mat[r][c-1])
    if c < shape[1] - 1 and not mat[r][c+1].processed:
            neighbors.append(mat[r][c+1])
    return neighbors
while len(pq) > 0:
    u=pq[0] #smallest-value unprocessed node
    #remove node of interest from the queue
    pq[0]=pq[-1] 
    pq[0].index_in_queue=0
    pq.pop()
    pq=bubble_down(pq,0) #min-heap function, see source code 
    
    u.processed=True
    neighbors = get_neighbors(matrix,u.y,u.x)
    for v in neighbors:
        dist=get_distance(img,(u.y,u.x),(v.y,v.x))
        if u.d + dist < v.d:
            v.d = u.d+dist
            v.parent_x=u.x #keep track of the shortest path
            v.parent_y=u.y
            idx=v.index_in_queue
            pq=bubble_down(pq,idx) 
            pq=bubble_up(pq,idx)
img = cv2.imread('maze.png') # read an image from a file using opencv (cv2) library
p = find_shortest_path(img, (25,5), (5,220))
drawPath(img,p)
plt.figure(figsize=(7,7))
plt.imshow(img) # show the image on the screen 
plt.show()'''