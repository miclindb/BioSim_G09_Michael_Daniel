from src.biosim.animals import Herbivore, Carnivore
from src.biosim.landscape import Jungle, Ocean, Mountain
import pandas as pd

"""

class AnnualCycle:
    landscape_dict = {'J': Jungle, 'O': Ocean, 'M': Mountain}

    def __init__(self):
        self.year = 0
        self.island_map = None

    def island_constructor(self, island_map):
        self.island_map = island_map
        cell = [landscape_dict[island_map]()]
        animal_objects = [Herbivore() for i in range(4)]
        cell.append(animal_objects)
        self.island_map = pd.DataFrame([[cell]])

    Do cell updates in own method.
"""


def feeding(animal_object):
    animal_species = animal_object.__class__.__name__
    if animal_species == 'Herbivore':
        animal_object.feed()
    elif animal_species == 'Carnivore':
        animal_object.kill()
    else:
        pass


def procreate(animal_object):
    pass


def migrate(animal_object):
    pass


def aging(animal_object):
    animal_object.age += 1


def loss_of_weight(animal_object):
    animal_object.weight -= (animal_object.weight * animal_object.parameters['eta'])
    animal_object.fitness = animal_object.calculate_fitness()


def death(animal_object):
    return animal_object.death()


def annual_cycle(animal_object, animal_species):
    """
    Performs operations related to the annual cycle for one cell.
    """
    feeding(animal_object, animal_species)  # Each animal feeds
    procreate(animal_object)  # Checks for birth for all animals
    migrate(animal_object)  # Each animal moves
    aging(animal_object)  # Updates age for all animals
    loss_of_weight(animal_object)  # Each animal loses weight
    death(animal_object)  # For each animal, we check if the animal dies
