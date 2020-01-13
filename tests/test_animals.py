# -*- coding: utf-8 -*-


__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore
import pytest
from pytest import approx

"""

class TestAnimals:
    @pytest.fixture(autouse=True)
    def animals_for_tests(self):
        self.herb = Herbivore()
        self.carn = Carnivore()
        
"""


def test_herbivore_default_class_initializer(self):
    """
    Tests that the class initializer for herbivore runs and uses default
    values when no inputs are provided
    """
    # herbivore = Herbivore()
    assert self.herb.age == 0
    assert isinstance(self.herb.age, int)
    assert self.herb.weight > 0
    assert isinstance(self.herb.weight, float)


def test_carnivore_default_class_initializer():
    """
    Tests that the class initializer for carnivore runs and uses default
    values when no inputs are provided
    """
    carnivore = Carnivore()
    assert carnivore.age == 0
    assert isinstance(carnivore.age, int)
    assert carnivore.weight > 0
    assert isinstance(carnivore.weight, float)


def test_herbivore_manual_input():
    """
    Tests that the class initializer for herbivore runs and uses inputs
    provided.
    """
    herbivore = Herbivore(10, 8)
    assert herbivore.age == 10
    assert herbivore.weight == 8


def test_carnivore_manual_input():
    """
    Tests that the class initializer for herbivore runs and uses inputs
    provided.
    """
    carnivore = Herbivore(10, 8)
    assert carnivore.age == 10
    assert carnivore.weight == 8


def test_calculate_weight():
    """
    Tests that 'calculate_weight' properly calculates the animal's weight.
    """
    # Need statistical tests


def test_calculate_fitness():
    """
    Tests that 'calculate_fitness' properly calculates the animal's fitness.
    Tested with weight as input in the initializer.
    """
    herbivore = Herbivore(weight=10)
    assert herbivore.fitness == approx(0.499832)


def test_getter_decorator():
    """
    Tests that the fitness getter returns the fitness value of the animal.
    """
    herbivore = Herbivore()
    assert herbivore.fitness == herbivore.get_fitness


def test_setter_decorator():
    """
    Tests that the fitness setter successfully updates the fitness of the
    animal.
    """
    herbivore = Herbivore()
    herbivore.get_fitness = 0.8
    assert herbivore.fitness == 0.8


def test_death_by_zero_fitness():
    """
    Tests that the animal dies upon reaching fitness = 0
    """
    herbivore = Herbivore()
    herbivore.get_fitness = 0
    assert bool(herbivore.death()) is True


def test_probability_of_death():
    pass


def test_gives_birth_returns_false():
    """
    Tests that gives_birth returns False if a baby is not successfully born.
    """
    herbivore = Herbivore(weight=3)
    assert herbivore.weight < herbivore.parameters['zeta'] * \
           (herbivore.parameters['w_birth'] + herbivore.parameters[
               'sigma_birth'])
    assert bool(herbivore.gives_birth(n=2, animal_object=herbivore)) is False


def test_gives_birth_returns_newborn():
    """
    Tests that gives_birth returns a new object of correct species when a baby
    is successfully born.
    """
    herbivore = Herbivore(weight=50)
    assert herbivore.weight >= herbivore.parameters['zeta'] * \
           (herbivore.parameters['w_birth'] + herbivore.parameters[
               'sigma_birth'])


def statistical_test_for_birth():
    """
    How to test for probability
    """
    pass


def test_herbivore_feeding_max_fodder():
    """
    Tests that the herbivore can eat and that it's weight is successfully
    updated.
    """
    herbivore = Herbivore(weight=2)
    cell_info_fodder = 500
    assert herbivore.feed(cell_info_fodder) == 10
    assert herbivore.weight == 11


def test_kill():
    """
    Tests that the carnivore can kill a nearby herbivore and that its weight
    and fitness is updated successfully.

    Fitness are manually set so that the carnivore will kill the herbivore with
    100% probability all times.

    After the carnivore kills, its weight should be increased and its
    (artificial) fitness should be reduced to a value between 0 and 1.
    """
    carn = Carnivore(age=2, weight=8)
    herb = Herbivore(age=2, weight=10)
    carn.get_fitness = 11
    herb.get_fitness = 0.5
    nearby_herbivores = [herb]
    x = carn.kill(nearby_herbivores)

    assert isinstance(x, list)
    assert len(x) == 1
    assert carn.weight > 8
    assert 0 < carn.fitness < 1
    assert carn.age == 2


def statistical_test_kill():
    """
    Tests the expected value for kill
    """
    pass


def kill_stops_at_eaten_is_f():
    pass


if __name__ == '__main__':
    pytest.main()
