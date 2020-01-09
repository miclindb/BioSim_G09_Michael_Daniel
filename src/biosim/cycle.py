from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Jungle, Ocean, Mountain
import pandas as pd


class AnnualCycle:
    landscape_dict = {'J': Jungle(), 'O': Ocean(), 'M': Mountain()}

    def __init__(self):
        self.year = 0
        self.island_map = None

    def island_constructor(self, island_map):
        self.island_map = island_map
        cell = [landscape_dict[map]]
        animal_objects = [Herbivore() for i in range(10)]
        cell.append(animal_objects)
        self.island_map = pd.DataFrame([[cell]])

    """
    Do cell updates in own method.
    """

    def feeding(self):
        pass

    def procreation(self):
        pass

    def migration(self):
        pass

    def aging(self):
        for x in range(self.island_map.shape[0]):
            for y in range(self.island_map.shape[1]):
                for animal in self.island_map[x][y][1]:
                    animal.age += 1

    def loss_of_weight(self):
        for x in range(self.island_map.shape[0]):
            for y in range(self.island_map.shape[1]):
                for animal in self.island_map[x][y][1]:
                    animal.weight -= (animal.weight * animal.parameters['eta'])
                    # animal.fitness = animal.calculate_fitness()

    def update_fitness(self):
        for x in range(self.island_map.shape[0]):
            for y in range(self.island_map.shape[1]):
                for animal in self.island_map[x][y][1]:
                    animal.fitness = animal.calculate_fitness()

    def death(self):
        for x in range(self.island_map.shape[0]):
            for y in range(self.island_map.shape[1]):
                for animal in self.island_map[x][y][1]:
                    dead = animal.death()
                    if dead is True:
                        self.island_map[x][y][1].remove(animal)




from biosim.animals import Herbivore, Carnivore

map = """\
         J"""

self.island_map = textwrap.dedent(map)

landscape_dict = {'J': Jungle(), 'O': Ocean(), 'M': Mountain()}

cell = [landscape_dict[map]]

animal_objects = [Herbivore() for i in range(10)]

cell.append(animal_objects)

df = pd.DataFrame([[cell]])
