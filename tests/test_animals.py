"""
Tests for animals file

"""
from src.biosim.animals import Herbivore, Carnivore


def test_herbivore_default_class_initializer():
    herbivore = Herbivore()
    assert herbivore.age == 0


def test_carnivore_default_class_initializer():
    carnivore = Carnivore()
    assert carnivore.age == 0


"""
@pytest
age = 10, weight = 8
For later, look this up
"""


def test_herbivore_manual_input():
    herbivore = Herbivore(10, 8)
    assert herbivore.age == 10
    assert herbivore.weight == 8
    # assert herbivore.fitness ==something


def test_carnivore_manual_input():
    carnivore = Herbivore(10, 8)
    assert carnivore.age == 10
    assert carnivore.weight == 8
    # assert carnivore.fitness ==something


def test_calculate_weight():
    pass


def test_calculate_fitness():
    pass


def test_death_by_zero_fitness():
    pass
    """
    herbivore = Herbivore(fitness=0)
    assert bool(herbivore.death()) != False
"""

def test_probablity_of_death():
    pass