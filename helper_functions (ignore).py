# Helper functions for main.py
import pygame
from random import choice, randrange
from main import *

class Food:
    def __init__(self):
        self.img = pygame.image.load('C:/Users/Shayaan/Downloads/Maze_Game-main/Maze_Game-main/images/food.jpg').convert() # loading the image
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

# Checking if the game is over when time remaining is less than 0 seconds.
def is_game_over():
    global time, score, record, FPS
    if time < 0:
        pygame.time.wait(700)
        player_rect.center = TILE // 2, TILE // 2
        [food.set_pos() for food in food_list]
        set_record(record, score)
        record = get_record()
        time, score, FPS = 30, 0, 60

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