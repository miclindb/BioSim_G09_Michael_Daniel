# -*- coding: utf-8 -*-

"""
Tests for animals module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.cell import Ocean, Mountain, Desert, Jungle, Savannah
import pytest
from pytest import approx
from scipy import stats


class TestAnimals:
    alpha = 0.05

    @pytest.fixture(autouse=True)
    def create_animals(self):
        """
        Setup for further animal tests.
        """
        self.herbivore = Herbivore(age=2, weight=10)
        self.carnivore = Carnivore(age=2, weight=10)
        self.new_herbivore = Herbivore()
        self.new_carnivore = Carnivore()

    def test_herbivore_default_class_initializer(self):
        """
        Tests that the class initializer for herbivore runs and uses default
        values when no inputs are provided
        """
        assert self.new_herbivore.age == 0
        assert isinstance(self.new_herbivore.age, int)
        assert self.new_herbivore.weight > 0
        assert isinstance(self.new_herbivore.weight, float)

    def test_carnivore_default_class_initializer(self):
        """
        Tests that the class initializer for carnivore runs and uses default
        values when no inputs are provided
        """
        assert self.new_carnivore.age == 0
        assert isinstance(self.new_carnivore.age, int)
        assert self.new_carnivore.weight > 0
        assert isinstance(self.new_carnivore.weight, float)

    def test_herbivore_manual_input(self):
        """
        Tests that the class initializer for herbivore runs and uses inputs
        provided.
        """
        assert self.herbivore.age == 2
        assert self.herbivore.weight == 10

    def test_carnivore_manual_input(self):
        """
        Tests that the class initializer for herbivore runs and uses inputs
        provided.
        """
        assert self.carnivore.age == 2
        assert self.carnivore.weight == 10

    def test_aging_method(self):
        """
        Tests that the 'aging' method successfully increases an animal's age
        by one year and updates its fitness.
        """
        fit = self.new_herbivore.fitness
        self.new_herbivore.aging()
        assert self.new_herbivore.age == 1
        assert self.new_herbivore.fitness < fit

    def test_calculate_weight_method(self):
        """
        Tests that 'calculate_weight' properly uses a normal distribution when
        calculating an animal's weight.

        The Shapiro-Wilks test is used for this. The significance level 'alpha'
        is set to 0.05. The 'p_value' is compared to the significance in order
        to determine whether the data is normally distributed.
        """
        weights = []
        for _ in range(500):
            ani = Herbivore()
            weight_calculation = ani.calculate_weight()
            weights.append(weight_calculation)

        shapiro = stats.shapiro(weights)
        p_value = shapiro[1]
        assert p_value > self.alpha

    def test_loss_of_weight(self):
        """
        Tests that the animal's weight is correctly reduced and that its
        fitness is updated.
        """
        self.herbivore.loss_of_weight()
        assert self.herbivore.weight == 9.5
        assert self.herbivore.fitness == approx(0.4872587)

    def test_weight_gain(self):
        """
        Tests that the method 'weight_gain" correctly calculates the amount of
        weight an animal should gain after eating a certain amount of fodder.
        """
        weight_gain = self.herbivore.weight_gain(eaten=10)
        assert weight_gain == 9.0

        weight_gain = self.carnivore.weight_gain(eaten=10)
        assert weight_gain == 7.5

    def test_calculate_fitness(self):
        """
        Tests that 'calculate_fitness' properly calculates the animal's
        fitness.
        """
        assert self.herbivore.fitness == approx(0.4997498)

    def test_update_fitness(self):
        """
        Tests that an animal's fitness is correctly updated.
        """
        assert self.herbivore.fitness == approx(0.4997498)
        self.herbivore.weight = 12
        self.herbivore.update_fitness()
        assert self.herbivore.fitness == approx(0.5495589)

    def test_fitness_getter_decorator(self):
        """
        Tests that the fitness getter returns the fitness value of the animal.
        """
        assert self.herbivore.fitness == self.herbivore.get_fitness

    def test_fitness_setter_decorator(self):
        """
        Tests that the fitness setter successfully updates the fitness of the
        animal.
        """
        self.herbivore.get_fitness = 0.8
        assert self.herbivore.fitness == 0.8


class TestDeath:

    @pytest.fixture(autouse=True)
    def create_animals(self):
        pass

    def test_death_by_zero_fitness(self):
        """
        Tests that the animal dies upon reaching fitness = 0.
        """
        self.herbivore.get_fitness = 0
        assert bool(self.herbivore.death()) is True

    def test_death_with_max_fitness(self):
        """
        Tests that an animal will not die if it has fitness = 1.
        The test is run for 100 herbivores with fitness = 1.
        """
        death_results = []
        herbs = [Herbivore() for _ in range(100)]
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


class TestBirth:

    @pytest.fixture()
    def create_animals(self):
        pass

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
        herb.adjust_weight_after_birth(self.new_herbivore)
        assert herb.weight == herb.weight - (
                herb.parameters['xi'] * self.new_herbivore.weight)

    def test_gives_birth_returns_none(self):
        """
        Tests that gives_birth passes if a baby is not successfully born.
        In the test, the mother's weight is manually set too low to birth a
        baby animal.
        """

        assert self.new_herbivore.weight < self.new_herbivore.weight_check_for_pregnancy()
        assert self.new_herbivore.gives_birth(n=2) is None

    def test_gives_birth_returns_newborn(self):
        """
        Tests that gives_birth returns a new object of correct species when a
        baby is successfully born.
        """
        herbivore = Herbivore(weight=50)
        assert herbivore.weight >= herbivore.weight_check_for_pregnancy()
        new_born = herbivore.gives_birth(n=500)
        assert isinstance(new_born, Herbivore)


class TestMigrate:

    @pytest.fixture(autouse=True)
    def setup_migrate(self):
        pass

    def test_check_move_return(self):
        """
        Tests that 'check_move' returns a bool.
        """
        check = self.herbivore.check_move()
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
        self.herbivore.get_fitness = 4
        assert self.herbivore.has_moved is False
        chosen_cell = self.herbivore.migrate(relative_fodder_list)
        assert bool(self.herbivore.check_move()) is True
        assert chosen_cell is None
        assert self.herbivore.has_moved is False

    def test_migrate_to_valid_cell(self):
        """
        Tests that the animal will migrate to a valid cell, and that its status
        'has_moved' is changed to 'True'. The Herbivore's fitness is set to
        four so that it always passes the 'check_move' check.

        relative_fodder_list is a list of tuple containing amount of fodder and
        corresponding cell object.
        """
        relative_fodder_list = [(50, Jungle()), (0, Ocean()), (0, Mountain())]
        herb.get_fitness = 4
        assert herb.has_moved is False
        chosen_cell = herb.migrate(relative_fodder_list)
        assert bool(herb.check_move()) is True
        assert isinstance(chosen_cell, Jungle)
        assert herb.has_moved is True


class TestFeedingKilling:

    @pytest.fixture(autouse=True)
    def create_animals(self):
        """
        Setup for 'feed' and 'kill' testing.
        """
        self.herbivore = Herbivore(weight=2)
        self.cell_full_fodder = 50.0
        self.cell_limited_fodder = 2.0

        self.nearby_herbivores = [Herbivore() for _ in range(10)]
        self.carnivore = Carnivore()
        #self.low_fit_carnivore = Carnivore().get_fitness = 0.001
        #self.low_fit_herbivore = Herbivore().get_fitness = 0.001

    def test_herbivore_feeding_max_fodder(self):
        """
        Tests that the herbivore can eat and that it's weight is successfully
        updated.
        """
        eaten = self.herbivore.feed(self.cell_full_fodder)
        assert eaten == 10
        assert self.herbivore.weight == 11.0

    def test_herbivore_feeding_limited_fodder(self):
        """
        Tests that the herbivore can eat if there is limited fodder, and that
        it's weight is successfully updated.
        """
        eaten = self.herbivore.feed(self.cell_limited_fodder)
        assert eaten == 2
        assert self.herbivore.weight == 3.8

    def test_fitness_greater_than_prey(self):
        """
        Tests that the method returns expected bool. If the fitness of the
        carnivore is greater than the fitness of the herbivore, and not greater
        than 'DeltaPhiMax', the method returns 'True'.
        """
        self.carnivore.parameters['DeltaPhiMax'] = 10.0
        assert self.carnivore.fitness > self.low_fit_carnivore.fitness
        assert bool(
            self.carnivore.fitness_greater_than_prey(self.low_fit_carnivore)
        ) is True

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

    def test_attempt_all_herbivore_kill(self):
        """
        Tests that the Carnivore attempts to kill all Herbivores nearby.
        """

    def test_kill_stops_at_eaten_is_f(self):
        """
        Tests that the carnivore stops eating.
        How can this be done?
        """
        carn = Carnivore(age=2, weight=8)
        nearby_herbs = [Herbivore(weight=2) for _ in range(10)]
        killed = carn.kill(nearby_herbs)
        assert len(killed) == 2
