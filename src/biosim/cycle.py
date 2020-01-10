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


def procreate(n, animal_object):
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
    animal_object.gives_birth(n, animal_object)


def migrate(animal_object):
    pass


def aging(animal_object):
    animal_object.age += 1


def loss_of_weight(animal_object):
    animal_object.weight -= (
            animal_object.weight * animal_object.parameters['eta']
    )
    animal_object.fitness = animal_object.calculate_fitness()


def death(animal_object):
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
    return animal_object.death()


def annual_cycle(animal_object, n):
    """
    Performs operations related to the annual cycle for one cell.
    """
   # feeding(animal_object)      # Each animal feeds
    procreate(n, animal_object)     # Checks for birth for all animals
    migrate(animal_object)      # Each animal moves
    aging(animal_object)        # Updates age for all animals
    loss_of_weight(animal_object)   # Each animal loses weight
    death(animal_object)        # For each animal, we check if the animal dies
