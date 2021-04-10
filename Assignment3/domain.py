# -*- coding: utf-8 -*-
import pickle
from copy import deepcopy
from random import *

import pygame

from utils import *
import numpy as np
from utils import *


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

class Gene:
    def __init__(self):
        # initialise the gene according to the reprezentation
        self.__coord = randint(1, 4)  # UP - 1, Right - 2, Down - 3, Left - 4


class Individual:
    def __init__(self, size=0): #size is given by the battery
        self.__size = size
        # self.__x = [gene() for i in range(self.__size)]
        self.__x = [randint(1, 4) for _ in range(self.__size)]
        self.__f = None

    def get_f(self):
        return self.__f

    def construct_path(self, current_map, drone): #phenotype of a chromosome (don't know if this expression is correct)
        path = [[drone[0], drone[1]]]

        for i in self.__x:
            if i == 1:
                path.append([path[-1][0] - 1, path[-1][1]])
            elif i == 2:
                path.append([path[-1][0], path[-1][1] + 1])
            elif i == 3:
                path.append([path[-1][0] + 1, path[-1][1]])
            elif i == 4:
                path.append([path[-1][0], path[-1][1] - 1])

        return path

    def fitness(self, current_map, drone):
        # compute the fitness for the individual
        # and save it in self.__f
        path = self.construct_path(current_map, drone)
        visited = []
        self.__f = 0
        broke_the_rules = False

        for i in range(len(path)):
            x = path[i][0]
            y = path[i][1]

            if [x, y] not in visited:
                visited.append([x, y])
                if x < 0 or y < 0 or current_map.n <= x or current_map.m <= y: #checks if wall or bad position
                    i -= 1
                    self.__f -= 2
                    continue
                if current_map.surface[x][y] == 1:
                    i -= 1
                    self.__f -= 2
                    continue

                self.__f += 1
                for direction in v: #discover
                    while ((0 <= x + direction[0] < current_map.n and 0 <= y + direction[1] < current_map.m) and
                           current_map.surface[x + direction[0]][y + direction[1]] != 1):
                        if [x + direction[0], y + direction[1]] not in visited:
                            visited.append([x + direction[0], y + direction[1]])
                            self.__f += 1
                        x = x + direction[0]
                        y = y + direction[1]

    def mutate(self, mutate_probability=0.04):
        if random() < mutate_probability:
            self.__x[randint(0, self.__size - 1)] = randint(1, 4) #change a gene in a chromosome, all random
            # perform a mutation with respect to the representation

    def crossover(self, other_parent, crossover_probability=0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossover_probability:
            index = randint(0, self.__size - 1) #try not only randomly but half-half
            offspring1.__x = other_parent.__x[:index] + self.__x[index:]
            offspring2.__x = self.__x[:index] + other_parent.__x[index:]
            # perform the crossover between the self and the otherParent 

        return offspring1, offspring2


class Population:
    def __init__(self, population_size=0, individual_size=0):
        self.__population_size = population_size
        self.__v = [Individual(individual_size) for _ in range(population_size)]

    def evaluate(self, map, drone):
        # evaluates the population
        for x in self.__v:
            x.fitness(map, drone)

    def compute_average_fitness_and_std(self, map, drone):
        fitness = []
        for x in self.__v:
            x.fitness(map, drone)
            fitness.append(x.get_f())
        return [np.average(fitness), np.std(fitness)]

    def set_individuals(self, individuals):
        self.__v = individuals

    def add_individual(self, individual, map, drone):
        individual.fitness(map, drone)
        self.__v.append(individual)

    def sort_individuals(self, individuals):
        sorted = False

        while not sorted:
            sorted = True
            for i in range(0, len(individuals) - 1):
                if individuals[i].get_f() < individuals[i + 1].get_f():
                    aux = individuals[i]
                    individuals[i] = individuals[i + 1]
                    individuals[i + 1] = aux
                    sorted = False

        return  individuals

    def get_first_path(self, map, drone):
        individuals_copy = deepcopy(self.__v)
        individuals_copy = self.sort_individuals(individuals_copy)
        return individuals_copy[0].construct_path(map, drone)


    def selection(self, k=0):
        # perform a selection of k individuals from the population
        # and returns that selection
        selected = []
        individuals_copy = deepcopy(self.__v)
        individuals_copy = self.sort_individuals(individuals_copy)

        for i in range(0, k):
            selected.append(individuals_copy[i])

        return selected


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def load_map(self, num_file):
        with open(num_file, "rb") as file:
            dummy = pickle.load(file)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            file.close()

    def save_map(self, file="test.map"):
        with open(file, "wb") as f:
            pickle.dump(self, f)
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine