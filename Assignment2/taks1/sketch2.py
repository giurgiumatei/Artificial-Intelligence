

# import the pygame module, so you can use it
import pickle,pygame,time
from math import sqrt

from pygame.locals import *
from random import random, randint
import numpy as np


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                
        return imagine        
        

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:        
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                 self.y = self.y + 1
                  
    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        
        return mapImage





def function_h(x2, x1, y2, y1): #cost heuristic function from the current state to the final state
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def function_g(x1, x3, y1, y3): #cost function from the initial state to the current state
    return sqrt((x1 - x3)**2 + (y1 - y3)**2)

def function_f(x2, x1, y2, y1, x3, y3): #cost estimation of the path
    result = function_h(x2, x1, y2, y1) + function_g(x1, x3, y1, y3)
    return result


def searchAStar(mapM, droneD, initialX, initialY, finalX, finalY):
    found = False  # false while no complete path was found
    visited = []  # cells visited, closed list
    to_visit = [(initialX, initialY)]  # priority queue, open list
    parent = {}
  #  path_cost= {}

    while to_visit and found == False:
        if not to_visit:
            return False

        cell = to_visit[-1]
        visited.append(cell)  # popped the cell and marked as visited
        current_x = cell[0]
        current_y = cell[1]
        del to_visit[-1]

        if current_x == finalX and current_y == finalY:
            found = True  # we check if we haven't got to the desired coordinates


        else:

            if current_x > 0 and mapM.surface[current_x - 1][current_y] == 0 and (current_x - 1, current_y) not in visited:

                if (current_x - 1, current_y) not in to_visit:
                    parent[(current_x - 1, current_y)] = cell
                    if (current_x-1, current_y) not in to_visit:
                        to_visit.append((current_x - 1, current_y))

            if current_y < 19 and mapM.surface[current_x][current_y + 1] == 0 and (current_x, current_y + 1) not in visited:

                if (current_x, current_y + 1) not in to_visit:
                    parent[(current_x, current_y+1)] = cell
                    if (current_x, current_y+1) not in to_visit:
                        to_visit.append((current_x, current_y+1))

            if current_x < 19 and mapM.surface[current_x + 1][current_y] == 0 and (current_x + 1, current_y) not in visited:

                if(current_x + 1, current_y) not in to_visit:
                    parent[(current_x + 1, current_y)] = cell
                    if (current_x + 1, current_y) not in to_visit:
                        to_visit.append((current_x + 1, current_y))

            if current_y > 0 and mapM.surface[current_x][current_y - 1] == 0 and (current_x, current_y - 1) not in visited:

                if (current_x, current_y - 1) not in to_visit:
                    parent[(current_x, current_y - 1)] = cell
                    if (current_x, current_y - 1) not in to_visit:
                        to_visit.append((current_x, current_y - 1))



           # to_visit = to_visit + aux
            to_visit = sorted(to_visit, key=lambda tup: function_h(finalX, tup[0], finalY, tup[1]), reverse=True)
            to_visit = sorted(to_visit, key=lambda tup: function_f(finalX, tup[0], finalY, tup[1], initialX, initialY), reverse=True)# sort by function f(...)
                                        # f(...)= h(...) + g(...)
                                        # we must sort twice so that in case
                                        # of equality of function f(...) we use
                                        # function h(...) as a secondary criterion

    path = []
    current_x = finalX
    current_y = finalY

    while ((current_x, current_y) in parent):
        path.append((current_x, current_y))
        aux_x = parent[(current_x, current_y)][0]
        aux_y = parent[(current_x, current_y)][1]
        current_x = aux_x
        current_y = aux_y
    path.append((initialX, initialY))

    return path






def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY):

    found = False #false while no complete path was found
    visited = [] #cells visited
    to_visit = [(initialX, initialY)] #priority queue
    parent = {}#here we store the parent of each node

    while to_visit and found == False:
        if not to_visit:
            return False

        cell = to_visit[-1]
        visited.append(cell) #popped the cell and marked as visited
        current_x = cell[0]
        current_y = cell[1]
        del to_visit[-1]

        if current_x == finalX and current_y == finalY:
            found = True #we check if we haven't got to the desired coordinates


        else:
            aux = [] #auxiliary list

            if current_x > 0 and mapM.surface[current_x - 1][current_y] == 0 and (current_x - 1, current_y) not in visited:
                parent[(current_x - 1, current_y)] = cell
                aux.append((current_x-1, current_y))

            if current_y < 19 and mapM.surface[current_x][current_y + 1] == 0 and (current_x, current_y + 1) not in visited:
                parent[(current_x, current_y + 1)] = cell
                aux.append((current_x, current_y+1))
            if current_x < 19 and mapM.surface[current_x + 1][current_y] == 0 and (current_x + 1, current_y) not in visited:
                parent[(current_x + 1, current_y)] = cell
                aux.append((current_x+1, current_y))

            if current_y > 0 and mapM.surface[current_x][current_y - 1] == 0 and (current_x, current_y - 1) not in visited:
                parent[(current_x, current_y - 1)] = cell
                aux.append((current_x, current_y-1))

            to_visit = to_visit + aux
            to_visit = sorted(to_visit, key=lambda tup: function_h(finalX, tup[0], finalY, tup[1]), reverse=True)#sort by euclidean distance
            #between state and final state
            #h(x)= sqrt((x2-x1)^2 + (y2-y1)^2)

    path = []
    current_x = finalX
    current_y = finalY

    while ((current_x, current_y) in parent):
        path.append((current_x, current_y))
        aux_x = parent[(current_x, current_y)][0]
        aux_y = parent[(current_x, current_y)][1]
        current_x = aux_x
        current_y = aux_y
    path.append((initialX, initialY))

    return path





def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]

def displayWithPath(image, path):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))

    return image


# define a main function
def main():

    # we create the map
    m = Map()
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")


    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    #create drona
    d = Drone(x, y)



    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)


    # define a variable to control the main loop




    screen.blit(d.mapWithDrone(m.image()),(0,0))
    pygame.display.flip()

    #path = dummysearch() #de schimbat aici
    path = searchAStar(m,d,0,3,19,19) #de schimbat aici
   # path = searchGreedy(m,d,0,3,19,19) #de schimbat aici
    screen.blit(displayWithPath(m.image(), path),(0,0))

    pygame.display.flip()
    time.sleep(60)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()