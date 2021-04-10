# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository:
    def __init__(self):

        self.__populations = []
        self.cmap = Map()
        self.drone = [0, 0]

    def create_population(self, args):
        # args = [populationSize, individualSize] -- you can add more args
        return Population(args[0], args[1])

    def add_population(self, population):
        self.__populations.append(population)

    def set_drone_coordinates(self, x, y):
        self.drone = [x, y]

    def add_individual(self, population, individual):
        population.add_individual(individual, self.cmap, self.drone)

    def evaluate_population(self, population):
        population.evaluate(self.cmap, self.drone)

    def get_current_population(self):
        return self.__populations[-1]

    def compute_average_fitness_and_std(self):
        return self.get_current_population().compute_average_fitness_and_std(self.cmap, self.drone)

    def get_first_path(self):
        return self.get_current_population().get_first_path(self.cmap, self.drone)

