# -*- coding: utf-8 -*-

"""
Tests for animals module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.cell import Ocean, Mountain, Desert, Jungle, Savannah
from pytest import approx
from scipy import stats

"""

class TestAnimals:
@pytest.fixture(autouse=True)
def animals_for_tests(self):
    self.herb = Herbivore()
    self.carn = Carnivore()
    
"""


class TestAnimals:
    """
    def __init__(self):
        self.herb = Herbivore()
        self.carn = Carnivore()
        self.herb_parameters = Herbivore.parameters
        self.carn_parameters = Carnivore.parameters
    """

    def test_herbivore_default_class_initializer(self):
        """
        Tests that the class initializer for herbivore runs and uses default
        values when no inputs are provided
        """
        herb = Herbivore()
        assert herb.age == 0
        assert isinstance(herb.age, int)
        assert herb.weight > 0
        assert isinstance(herb.weight, float)

    def test_carnivore_default_class_initializer(self):
        """
        Tests that the class initializer for carnivore runs and uses default
        values when no inputs are provided
        """
        carnivore = Carnivore()
        assert carnivore.age == 0
        assert isinstance(carnivore.age, int)
        assert carnivore.weight > 0
        assert isinstance(carnivore.weight, float)

    def test_herbivore_manual_input(self):
        """
        Tests that the class initializer for herbivore runs and uses inputs
        provided.
        """
        herbivore = Herbivore(10, 8)
        assert herbivore.age == 10
        assert herbivore.weight == 8

    def test_carnivore_manual_input(self):
        """
        Tests that the class initializer for herbivore runs and uses inputs
        provided.
        """
        carnivore = Herbivore(10, 8)
        assert carnivore.age == 10
        assert carnivore.weight == 8

    def test_aging_method(self):
        """
        Tests that the 'aging' method successfully increases an animal's age
        by one year and updates its fitness.
        """
        herbivore = Herbivore(age=5)
        fit = herbivore.fitness
        herbivore.aging()
        assert herbivore.age == 6
        assert herbivore.fitness < fit

    def test_calculate_weight_method(self):
        """
        Tests that 'calculate_weight' properly uses a normal distribution when
        calculating an animal's weight.

        The Shapiro-Wilks test is used for this. The significance level 'alpha'
        is set to 0.05. The 'p_value' is compared to the significance in order
        to determine whether the data is normally distributed.
        """
        alpha = 0.05
        weights = []
        for _ in range(500):
            ani = Herbivore()
            weight_calculation = ani.calculate_weight()
            weights.append(weight_calculation)

        shapiro = stats.shapiro(weights)
        p_value = shapiro[1]
        assert p_value > alpha

    def test_loss_of_weight(self):
        """
        Tests that the animal's weight is correctly reduced and that its
        fitness is updated.
        """
        herb = Herbivore(age=2, weight=10)
        herb.loss_of_weight()
        assert herb.weight == 9.5
        assert herb.fitness == approx(0.5122410)

    def test_weight_gain(self):
        """
        Tests that the method 'weight_gain" correctly calculates the amount of
        weight an animal should gain after eating a certain amount of fodder.
        """
        herb = Herbivore(age=2, weight=10)
        weight_gain = herb.weight_gain(eaten=10)
        assert weight_gain == 9.0

        carn = Carnivore(age=2, weight=10)
        weight_gain = carn.weight_gain(eaten=10)
        assert weight_gain == 7.5

    def test_calculate_fitness(self):
        """
        Tests that 'calculate_fitness' properly calculates the animal's
        fitness.
        """
        herbivore = Herbivore(age=0, weight=10)
        assert herbivore.fitness == approx(0.499832)

    def test_update_fitness(self):
        """
        Tests that an animal's fitness is correctly updated.
        """
        herb = Herbivore(age=0, weight=10)
        assert herb.fitness == approx(0.499832)
        herb.weight = 12
        herb.update_fitness()
        assert herb.fitness == approx(0.450015)

    def test_fitness_getter_decorator(self):
        """
        Tests that the fitness getter returns the fitness value of the animal.
        """
        herbivore = Herbivore()
        assert herbivore.fitness == herbivore.get_fitness

    def test_fitness_setter_decorator(self):
        """
        Tests that the fitness setter successfully updates the fitness of the
        animal.
        """
        herbivore = Herbivore()
        herbivore.get_fitness = 0.8
        assert herbivore.fitness == 0.8

    def test_death_by_zero_fitness(self):
        """
        Tests that the animal dies upon reaching fitness = 0.
        """
        herbivore = Herbivore()
        herbivore.get_fitness = 0
        assert bool(herbivore.death()) is True

    def test_death_with_max_fitness(self):
        """
        Tests that an animal will not die if it has fitness = 1.
        The test is run for 1000 herbivores with fitness = 1.
        """
        death_results = []
        herbs = [Herbivore() for _ in range(1000)]
        for herb in herbs:
            herb.get_fitness = 1
            dead = herb.death()
            death_results.append(dead)

        assert True not in death_results

    def test_probability_of_death(self):
        """
        WRONG: Tests the binomial distribution of animal deaths. The tests is
        performed on several animals, where the expected number of dead
        animals is asserted.

        Returns
        -------
        This is not done!!!
        """
        pass
        alpha = 0.05
        herbs = [Herbivore() for _ in range(500)]
        data = []
        for herb in herbs:
            data.append(herb.death())

        expected_distribution = stats.binom_test(x=2, n=500, p=0.02)
        assert p_value > alpha

    def test_weight_check_for_pregnancy(self):
        """
        Tests that the weight check is passed whenever the weight of the animal
        is above the set threshold.
        """
        herb_1 = Herbivore(weight=40)
        herb_2 = Herbivore(weight=10)
        carn_1 = Carnivore(weight=25)
        carn_2 = Carnivore(weight=8)
        assert herb_1.weight >= herb_1.weight_check_for_pregnancy()
        assert herb_2.weight < herb_2.weight_check_for_pregnancy()
        assert carn_1.weight >= carn_1.weight_check_for_pregnancy()
        assert carn_2.weight < carn_2.weight_check_for_pregnancy()

    def test_probability_of_birth(self):
        """
        Tests that the probability of birth returns correctly.
        Statistical tests?
        """
        pass
        herb = Herbivore()
        carn = Carnivore()

    def test_adjust_weight_after_birth(self):
        """
        Tests that the weight of the mother is correctly updated after method
        is called.
        """
        herb = Herbivore(weight=40)
        new_born = Herbivore(weight=6)
        herb.adjust_weight_after_birth(new_born)
        assert herb.weight == 32.8

    def test_gives_birth_returns_none(self):
        """
        Tests that gives_birth passes if a baby is not successfully born.
        In the test, the mother's weight is manually set too low to birth a
        baby animal.
        """
        herbivore = Herbivore(weight=3)
        assert herbivore.weight < herbivore.weight_check_for_pregnancy()
        assert herbivore.gives_birth(n=2) is None

    def test_gives_birth_returns_newborn(self):
        """
        Tests that gives_birth returns a new object of correct species when a
        baby is successfully born.
        """
        herbivore = Herbivore(weight=50)
        assert herbivore.weight >= herbivore.weight_check_for_pregnancy()
        new_born = herbivore.gives_birth(n=500)
        assert isinstance(new_born, Herbivore)

    def test_check_move_return(self):
        """
        Tests that 'check_move' returns a bool.
        """
        herb = Herbivore()
        check = herb.check_move()
        assert isinstance(check, bool)

    def test_statistical_test_check_move(self):
        """
        Tests that a dataset of multiple tests on 'check_move' is a binomial
        distribution.
        """
        pass

    def test_migrate_returns_none_for_invalid_cells(self):
        """
        Tests that 'migrate' returns None whenever the animal attempts to move
        to a invalid cell, and that its status 'has_moved' is changed to
        'True'. The Herbivore's fitness is set to four so that it always passes
        the 'check_move' check.

        relative_fodder_list is a list of tuple containing amount of fodder and
        corresponding cell object.
        """
        relative_fodder_list = [(0, Ocean()), (0, Mountain())]
        herb = Herbivore()
        herb.get_fitness = 4
        assert herb.has_moved is False
        chosen_cell = herb.migrate(relative_fodder_list)
        assert bool(herb.check_move()) is True
        assert chosen_cell is None
        assert herb.has_moved is False

    def test_migrate_to_valid_cell(self):
        """
        Tests that the animal will migrate to a valid cell, and that its status
        'has_moved' is changed to 'True'. The Herbivore's fitness is set to
        four so that it always passes the 'check_move' check.

        relative_fodder_list is a list of tuple containing amount of fodder and
        corresponding cell object.
        """
        relative_fodder_list = [(50, Jungle()), (0, Ocean()), (0, Mountain())]
        herb = Herbivore()
        herb.get_fitness = 4
        assert herb.has_moved is False
        chosen_cell = herb.migrate(relative_fodder_list)
        assert bool(herb.check_move()) is True
        assert isinstance(chosen_cell, Jungle)
        assert herb.has_moved is True

    def test_herbivore_feeding_max_fodder(self):
        """
        Tests that the herbivore can eat and that it's weight is successfully
        updated.
        """
        herbivore = Herbivore(weight=2)
        cell_fodder = 50.0
        eaten = herbivore.feed(cell_fodder)
        assert eaten == 10
        assert herbivore.weight == 11.0

    def test_herbivore_feeding_limited_fodder(self):
        """
        Tests that the herbivore can eat if there is limited fodder, and that
        it's weight is successfully updated.
        """
        herbivore = Herbivore(weight=2)
        cell_fodder = 2.0
        eaten = herbivore.feed(cell_fodder)
        assert eaten == 2
        assert herbivore.weight == 3.8

    def test_fitness_greater_than_prey(self):
        """
        Tests that the method returns expected bool. If the fitness of the
        carnivore is greater than the fitness of the herbivore, and not greater
        than 'DeltaPhiMax', the method returns 'True'.
        """
        carn = Carnivore(weight=8)
        carn.parameters['DeltaPhiMax'] = 10.0
        herb = Herbivore(weight=100)
        assert carn.fitness > herb.fitness
        assert bool(carn.fitness_greater_than_prey(herb)) is True

    def test_chance_of_kill_check(self):
        """
        Tests that 'chance_of_kill' returns an expected value.
        """
        carn = Carnivore(weight=8)
        carn.parameters['DeltaPhiMax'] = 10.0
        herb = Herbivore(weight=100)
        assert carn.chance_of_kill(herb) == approx(0.01678582)

    def test_kill_one_herbivore(self):
        """
        Tests that the carnivore can kill a nearby herbivore and that its
        weight and fitness is updated successfully after.

        Fitness is manually set in this test so that the carnivore will kill
        a herbivore with 100% probability.

        After the carnivore kills, its weight is increased and its
        (artificial) fitness should be reduced to a value between 0 and 1.
        """
        carn = Carnivore(age=2, weight=8)
        herb = [Herbivore(age=2, weight=10)]
        carn.get_fitness = 11
        x = carn.kill(herb)

        assert isinstance(x, list)
        assert isinstance(x[0], Herbivore)
        assert len(x) == 1
        assert carn.weight > 8
        assert 0 < carn.fitness < 1

    def statistical_test_kill(self):
        """
        Tests the expected value for kill
        """
        pass

    def test_kill_stops_at_eaten_is_f(self):
        """
        Tests that the carnivore stops eating.
        How can this be done?
        """
        carn = Carnivore(age=2, weight=8)
        nearby_herbs = [Herbivore(weight=2) for _ in range(10)]
        killed = carn.kill(nearby_herbs)
        assert len(killed) == 2
