import time

from repository import *


class Controller:
    def __init__(self, repository):
        # args - list of parameters needed in order to create the controller
        self._number_of_seeds = None
        self._repository = repository
        self._steps = None
        self._population_size = None
        self._number_of_iterations = None
        self._mutation_probability = None
        self._crossover_probability = None
        self._iteration = 0
        self._statistics = [] #avg fitness and std

    def iteration(self, args=0):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        print("Iteration " + str(self._iteration)) #move this in ui

        self._iteration += 1

        population = self._repository.get_current_population()
        self._repository.evaluate_population(population)
        select = population.selection(self._population_size - 2)
        parents = select[:len(select) // 2]
        pairs = len(parents) // 2
        used_pairs = []

        for i in range(pairs):
            first_parent = parents[randint(0, len(parents) - 1)]
            second_parent = parents[randint(0, len(parents) - 1)]

            if [first_parent, second_parent] not in used_pairs:
                used_pairs.append([first_parent, second_parent])
                first_crossed, second_crossed = first_parent.crossover(second_parent, self._crossover_probability)
                first_parent.mutate(self._mutation_probability)
                second_crossed.mutate(self._mutation_probability)
                self._repository.add_individual(population, first_crossed)
                self._repository.add_individual(population, second_crossed)

        population.set_individuals(select)

    def run(self, args=0):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics
        
        # return the results and the info for statistics
        fitness_stat = []
        stats = []

        for i in range(0, self._number_of_iterations):
            self.iteration()
            stats.append(self._repository.compute_average_fitness_and_std())
            print(stats) #to be moved in the ui

        for i in stats:
            fitness_stat.append(i[0])

        self._statistics.append([np.average(fitness_stat), np.std(fitness_stat)])

    def solver(self, args=0):
        # args - list of parameters needed in order to run the solver
        
        # create the population,
        # run the algorithm
        # return the results and the statistics

        start_time = time.time()
        for i in range(self._number_of_seeds):
            seed(30 - i)
            population = self._repository.create_population([self._population_size, self._steps])
            self._repository.add_population(population)
            self.run()
            print(self._statistics[i]) #to be moved in the ui

        print("--- %.2f seconds ---" % (time.time() - start_time))
        return self._repository.get_first_path(), self._statistics

    def set_seed_number(self, number_of_seeds):
        self._number_of_seeds = number_of_seeds

    def set_drone_coordinates(self, x, y):
        self._repository.set_drone_coordinates(x, y)

    def set_steps(self, number_of_steps):
        self._steps = number_of_steps

    def set_crossover_probability(self, probability):
        self._crossover_probability = probability

    def set_mutation_probability(self, probability):
        self._mutation_probability = probability

    def set_number_of_iterations(self, number_of_iterations):
        self._number_of_iterations = number_of_iterations

    def set_population_size(self, size):
        self._population_size = size

    def map_with_drone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (0, 0))

        return mapImage

