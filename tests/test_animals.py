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
    Tests if the animal dies upon reaching fitness = 0
    """
    herbivore = Herbivore()
    herbivore.get_fitness = 0
    assert bool(herbivore.death()) is True


def test_probability_of_death():
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
