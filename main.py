from pygame import *
from random import *
from os import *
# Starting up pygame and necessary components
environ['SDL_VIDEO_CENTERED'] = '1'
init()
size = width, height = 800, 600
screen = display.set_mode(size)
# Declaring colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Declaring variables

menu = "game"
marioPos = [0, 0, 0, 0]

# Declaring main functions

def game():
    pass

def menu():
    pass

def loading():
    pass

def instructions():
    pass
running = True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False

    mb = mouse.get_pressed()
    mx, my = mouse.get_pos()
    display.flip()

quit()
