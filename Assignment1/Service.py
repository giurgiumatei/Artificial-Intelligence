

# import the pygame module, so you can use it

from random import random, randint
import time
from Drone import *


# define a main function
def start():
    #we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    #print(str(e))

    # we create the map
    m = DMap()


    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")



    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    #cream drona
    d = Drone(x, y)



    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800,400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0, 0))

    # define a variable to control the main loop
    running = True
    stack.append((x, y))

    # main loop

    while running:

        m.markDetectedWalls(e, d.x, d.y)
        d.moveDSF(m)
        screen.blit(m.image(d.x, d.y), (400, 0))
        pygame.display.flip()
        time.sleep(0.3)
        if not stack:
            running = False



    pygame.quit()

