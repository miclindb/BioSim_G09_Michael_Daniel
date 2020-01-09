"""
Tests for animals file

"""
from src.biosim.animals import Herbivore, Carnivore

"""
@pytest.fixture
def make_test_animals(self):
    self.
"""


def test_herbivore_default_class_initializer():
    """
    Tests that the class initializer for herbivore runs and uses default
    values when no inputs are provided
    Returns
    -------

    """
    herbivore = Herbivore()
    assert herbivore.age == 0
    assert isinstance(herbivore.age, int)
    assert herbivore.weight > 0
    assert isinstance(herbivore.weight, float)


def test_carnivore_default_class_initializer():
    """
    Tests that the class initializer for herbivore runs and uses default
    values when no inputs are provided
    Returns
    -------

    """
    carnivore = Carnivore()
    assert carnivore.age == 0
    assert isinstance(carnivore.age, int)
    assert carnivore.weight > 0
    assert isinstance(carnivore.weight, float)


def test_herbivore_manual_input():
    herbivore = Herbivore(10, 8)
    assert herbivore.age == 10
    assert herbivore.weight == 8


def test_carnivore_manual_input():
    carnivore = Herbivore(10, 8)
    assert carnivore.age == 10
    assert carnivore.weight == 8


def test_calculate_weight():
    pass


def test_calculate_fitness():
    pass


def test_getter_decorator():
    herbivore = Herbivore()
    assert herbivore.fitness == herbivore.get_fitness


def test_setter_decorator():
    herbivore = Herbivore()
    herbivore.get_fitness = 0.8
    assert herbivore.fitness == 0.8


def test_death_by_zero_fitness():
    """
    Checks if the animal dies upon reaching fitness = 0
    Returns
    -------

    """
    herbivore = Herbivore()
    herbivore.get_fitness = 0
    assert bool(herbivore.death()) is True


def test_probability_of_death():
    pass
