"""
Tests for cycle.py
"""
from src.biosim.animals import Herbivore, Carnivore
import src.biosim.cycle as cycle
from pytest import approx


def test_annual_cycle():
    """
    Testing that self.island_map is 'None' when initializing the
    AnnualCycle class.
    """
    # test_cycle = cycle.AnnualCycle()
    # assert test_cycle.island_map is None
    pass


def test_feeding():
    """
    Tests that the animal's weight and fitness is updated after feeding.
    Cell fodder should be reduced.
    """
    some_herbivore = Herbivore(age=10, weight=10)
    eaten = cycle.feeding(animal_object=some_herbivore, cell_fodder=800)
    assert some_herbivore.weight == 19
    assert some_herbivore.fitness == approx(0.2883357)
    # assert cell_fodder ==


def test_procreate():
    """
    Need to see statistical tests
    """
    pass


def test_migrate():
    pass


def test_aging():
    """
    Tests that aging increases the age of the animal and then updates its
    fitness. Also tests that weight is not changed.

    The fitness only slightly changes whenever an animal age increase by 1.
    """
    some_herbivore = Herbivore(age=10, weight=10)
    some_carnivore = Carnivore(age=10, weight=10)
    ini_fitness_herb = some_herbivore.fitness
    ini_fitness_carn = some_carnivore.fitness
    cycle.aging(some_herbivore)
    cycle.aging(some_carnivore)
    assert some_herbivore.age == 11
    assert some_carnivore.age == 11
    assert some_herbivore.weight == 10
    assert some_carnivore.weight == 10
    assert some_herbivore.fitness == approx(0.498490790)
    assert some_carnivore.fitness == approx(0.083172696)
    assert ini_fitness_herb != some_herbivore.fitness
    assert ini_fitness_carn != some_carnivore.fitness


def test_loss_of_weight():
    """
    Tests that an animal loses weight after loss_of_weight is called and
    that its fitness is updated after. Also tests that age is not changed.
    """
    some_herbivore = Herbivore(age=10, weight=10)
    some_carnivore = Carnivore(age=10, weight=10)
    ini_fitness_herb = some_herbivore.fitness
    ini_fitness_carn = some_carnivore.fitness
    cycle.loss_of_weight(some_herbivore)
    cycle.loss_of_weight(some_carnivore)
    assert some_herbivore.age == 10
    assert some_carnivore.age == 10
    assert some_herbivore.weight == 9.5
    assert some_carnivore.weight == 8.75
    assert ini_fitness_herb != some_herbivore.fitness
    assert ini_fitness_carn != some_carnivore.fitness


def test_death():
    """
    Tests that an animal dies when its fitness is 0.
    """
    herbivore = Herbivore()
    herbivore.get_fitness = 0
    assert bool(herbivore.death()) is True



