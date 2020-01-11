from src.biosim.animals import Herbivore, Carnivore
from src.biosim.landscape import Jungle, Ocean, Mountain
import pandas as pd
import numpy as np

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
"""
class AnnualCycle:
    def __init__(self, animal, n):
        self.animal = animal
        self.n = n
"""


def feeding(animal_object, cell_fodder):
    animal_species = animal_object.__class__.__name__
    if animal_species == 'Herbivore':
        animal_object.feed(cell_fodder)
    elif animal_species == 'Carnivore':
        animal_object.kill()
    else:
        pass


def procreate(cell_population, animal_object, n):
    """
    Annual birth.

    Parameters
    ----------
    n: int
        Number of nearby animals.
    animal_object: class object
        Object of the animal.

    Returns: Bool or class object
        False if birth is unsuccessful
        class object if a new baby is successfully born.
    -------

    """
    birth = animal_object.gives_birth(animal_object, n)

    if birth is None:
        pass
    elif birth[0] is True:
        cell_population.append(birth[1])


def migrate(animal_object):
    pass
g

def aging(animal_object):
    animal_object.age += 1
    animal_object.update_fitness()


def loss_of_weight(animal_object):
    animal_object.weight -= (
            animal_object.weight * animal_object.parameters['eta']
    )
    animal_object.update_fitness()


def death(cell_population, animal_object):
    """
    Checks if an animal dies.

    Parameters
    ----------
    animal_object: class object
        Object for animal

    Returns: Bool
        'True' is the animal dies and 'False' otherwise.
    -------

    """
    animal_fitness = float(animal_object.fitness)
    if animal_fitness == 0:
        cell_population.remove(animal_object)
    elif np.random.uniform(0, 1) <= animal_object.parameters['omega'] * (
           1.0 - animal_fitness):
        cell_population.remove(animal_object)
    else:
        pass


def annual_cycle(cell_population, cell_fodder, animal_object, n):
    """
    Performs operations related to the annual cycle for one cell.
    """
    feeding(animal_object, cell_fodder)      # Each animal feeds
    procreate(cell_population, animal_object, n)     # Checks for birth for all animals
    migrate(animal_object)      # Each animal moves
    aging(animal_object)        # Updates age for all animals
    loss_of_weight(animal_object)   # Each animal loses weight
    death(cell_population, animal_object)        # For each animal, we check if the animal dies
