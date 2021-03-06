# -*- coding: utf-8 -*-


# imports
import pygame
import matplotlib
import matplotlib.pyplot as plt
from gui import *
from controller import *
from repository import *
from domain import *


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class UI:
    def __init__(self, controller, repository):
        self._controller = controller
        self._repository = repository
        self._path = []
        self._stats = []
        self.__iterations = []

    def print_first_menu(self):
        print("1. load map")
        print("2. next menu")

    def print_second_menu(self):
        print("1. parameters setup")
        print("2. run the solver")
        print("3. visualise the statistics")
        print("4. view the drone moving on a path")

    def print_menu(self):
        print("1. load map")
        print("2. load parameters")
        print("3. run the solver")
        print("4. view statistics")
        print("5. view the drone moving")


    def parameters_setup(self):
        print("Filename: ")
        file = input()

        f = open(file, 'r')
        i = 0
        for line in f:
            if i == 0:
                line = line.rstrip()
                l = line.split(",")
                self._controller.set_drone_coordinates(int(l[0]), int(l[1]))
            elif i == 1:
                line = line.rstrip()
                self._controller.set_steps(int(line))
            elif i == 2:
                line = line.rstrip()
                self._controller.set_number_of_iterations(int(line))
            elif i == 3:
                line = line.rstrip()
                self._controller.set_population_size(int(line))
            elif i == 4:
                line = line.rstrip()
                self._controller.set_mutation_probability(float(line))
            elif i == 5:
                line = line.rstrip()
                self._controller.set_crossover_probability(float(line))
            elif i == 6:
                line = line.rstrip()
                self._controller.set_seed_number(int(line))
            else:
                break
            i += 1
        f.close()

    def run_solver(self):
        self._path, self._stats = self._controller.solver()
        print(self._stats)
        self.view_drone_moving()

    def view_statistics(self):
        x = []
        average = []
        deviations = []
        for i in range(len(self._stats)):
            x.append(i)
            average.append(self._stats[i][0])
            deviations.append(self._stats[i][1])
        plt.plot(x, average)
        plt.plot(x, deviations)
        plt.show()


    def load_map(self):
        print("Map title:")
        numfile = input()
        self._repository.cmap.load_map(numfile)

    def menu(self):

        while True:
            self.print_menu()
            option = int(input())
            if option == 1:
                self.load_map()
            elif option == 2:
                self.parameters_setup()
            elif option == 3:
                self.run_solver()
            elif option == 4:
                self.view_statistics()
            elif option == 5:
                self.view_drone_moving()
            else:
                print("Invalid option")


    def initPyGame(self, dimension):
        # init the pygame
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration with EA")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode(dimension)
        screen.fill(WHITE)
        return screen


    def closePyGame(self):
        # closes the pygame
        running = True
        # loop for events
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()

    def view_drone_moving(self):
        movingDrone(self._repository.cmap, self._path, 0.2)

    def moving_drone(self, currentMap, path, speed=1, mark_explored=True):
        # animation of a drone on a path

        screen = initPyGame((currentMap.n * 20, currentMap.m * 20))

        drona = pygame.image.load("drona.png")

        for i in range(len(path)):
            screen.blit(image(currentMap), (0, 0))

            if mark_explored:
                brick = pygame.Surface((20, 20))
                brick.fill(GREEN)
                for j in range(i + 1):
                    for var in v:
                        x = path[j][0]
                        y = path[j][1]
                        while ((0 <= x + var[0] < currentMap.n and
                                0 <= y + var[1] < currentMap.m) and
                               currentMap.surface[x + var[0]][y + var[1]] != 1):
                            x = x + var[0]
                            y = y + var[1]
                            screen.blit(brick, (y * 20, x * 20))

            screen.blit(drona, (path[i][0] * 20, path[i][1] * 20))
            pygame.display.flip()
            time.sleep(0.5 * speed)
        self.closePyGame()


    def image(self, currentMap, colour=BLUE, background=WHITE):
        # creates the image of a map

        imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
        brick = pygame.Surface((20, 20))
        brick.fill(colour)
        imagine.fill(background)
        for i in range(currentMap.n):
            for j in range(currentMap.m):
                if (currentMap.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine
