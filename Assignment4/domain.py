import random


class Ant:
    def __init__(self, starting_sensor, energy=150):
        self.path = []
        self.energy_given = [] # how much energy for each sensor
        self.visited_sensors = [starting_sensor]
        self.energy = energy

    '''
        alegem sensor
        merem la altu - daca ii aproape si daca putem
    '''

    def choose_sensor(self, map, distances_between_sensors,  pheromone_level, sensors_visibility, alpha=0.8, beta=1.5):
    #3. Determine using ACO the shortest path between the sensors
        last_sensor = self.visited_sensors[-1]

        possible_sensors = []#list of sensors that can be visited

        for sensor_tuple in distances_between_sensors: #A star distance between each 2 sensors, in the beginning pheromone level is 0
            if sensor_tuple[0] == last_sensor and sensor_tuple[1] not in self.visited_sensors:#append whichever sensor hasn't been visited
                possible_sensors.append([sensor_tuple[1], distances_between_sensors[sensor_tuple]])
            if sensor_tuple[1] == last_sensor and sensor_tuple[0] not in self.visited_sensors:
                possible_sensors.append([sensor_tuple[0], distances_between_sensors[sensor_tuple]])

        desirability = []
        for s in possible_sensors:
            key = (s[0], last_sensor)
            if key not in pheromone_level.keys():
                key = (last_sensor, s[0])
            distance = s[1].Length
            if distance <= self.energy:# computes how prone the ant is to go at a specific sensor based on distance and pheromone level
                if pheromone_level[key] != 0:
                    desirability.append((1 / distance ** beta) * (pheromone_level[key] ** alpha))
                else:
                    desirability.append((1 / distance ** beta))

        # roulette
        s = sum(desirability)

        if s == 0:
            return "No more sensors"
        p = [desirability[i]/s for i in range(len(desirability))]
        p = [sum(p[0:i+1]) for i in range(len(p))]
        r = random.random()
        i = 0
        while r > p[i]:
            i = i+1
        the_chosen_one = possible_sensors[i][0]

        self.visited_sensors.append(the_chosen_one)

        key = (the_chosen_one, last_sensor)
        if key not in pheromone_level:
            key = (last_sensor, the_chosen_one)

        pheromone_level[key] += 1
        self.energy -= distances_between_sensors[key].Length

        return the_chosen_one


class Path:
    def __init__(self, path):
        self.path = path
        self.length = len(path)
        self.pheromone_level = []

    @property
    def Length(self):
        return self.length
