# -*- coding: utf-8 -*-

"""
Tests for cell module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import pytest
from biosim.cell import Cell, Ocean, Mountain, Jungle, Savannah, Desert
from biosim.animals import Animals, Carnivore, Herbivore
from biosim.simulation import BioSim


class TestCellOperations:
    """
    Tests for operations in cell.
    """

    DEFAULT_HERBIVORE_PARAMS = {
        'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
        'a_half': 40.0, 'phi_age': 0.2, 'w_half': 10.0, 'phi_weight': 0.1,
        'mu': 0.25, 'lambda': 1.0, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
        'omega': 0.4, 'F': 10.0
    }

    DEFAULT_CARNIVORE_PARAMS = {
        'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125,
        'a_half': 60.0, 'phi_age': 0.4, 'w_half': 4.0, 'phi_weight': 0.4,
        'mu': 0.4, 'lambda': 1.0, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
        'omega': 0.9, 'F': 50.0, 'DeltaPhiMax': 10.0
    }

    DEFAULT_JUNGLE_PARAMS = {
        'f_max': 800
    }

    DEFAULT_SAVANNAH_PARAMS = {
        'f_max': 300.0, 'alpha': 0.3
    }

    @pytest.fixture(autouse=True)
    def reset_all_params(self):
        """
        Sets all parameters to default values after each test in this suite
        so that changes will not remain for other test-modules.

        Note: might throw an error if set_animal_parameters() and set_landscape_parameters()
              are not implemented
        """
        yield
        BioSim.set_animal_parameters("Herbivore", self.DEFAULT_HERBIVORE_PARAMS)
        BioSim.set_animal_parameters("Carnivore", self.DEFAULT_CARNIVORE_PARAMS)
        BioSim.set_landscape_parameters("J", self.DEFAULT_JUNGLE_PARAMS)
        BioSim.set_landscape_parameters("S", self.DEFAULT_SAVANNAH_PARAMS)

    @pytest.fixture(autouse=True)
    def setup_cells(self, mocker):
        """
        Setup for cell tests.
        """
        self.ocean_cell = Ocean()
        self.jungle_cell = Jungle()
        self.savannah_cell = Savannah()
        self.mountain_cell = Mountain()
        self.desert_cell = Desert()
        self.single_herb = Herbivore()
        self.single_carn = Carnivore()
        self.single_pop = [Herbivore()]
        self.test_pop = [Carnivore(age=2, weight=20),
                         Herbivore(age=2, weight=20),
                         Herbivore(age=2, weight=40),
                         Herbivore(age=2, weight=10)]

        self.herb_pop = [Herbivore(age=2, weight=40),
                         Herbivore(age=2, weight=40),
                         Herbivore(age=2, weight=40),
                         Herbivore(age=2, weight=40)]

        self.carn_pop = [Carnivore(age=2, weight=20),
                         Carnivore(age=2, weight=20),
                         Carnivore(age=2, weight=40),
                         Carnivore(age=2, weight=10)]

        # Setup for mocking
        self.mock_feed_herbivore = mocker.spy(Herbivore, 'feed')
        self.mock_feed_carnivore = mocker.spy(Carnivore, 'kill')
        self.mock_procreate = mocker.spy(Animals, 'gives_birth')
        self.mock_migrate = mocker.spy(Animals, 'migrate')
        self.mock_aging = mocker.spy(Animals, 'aging')
        self.mock_loss_of_weight = mocker.spy(Animals, 'loss_of_weight')
        self.mock_deaths = mocker.spy(Animals, 'death')

    def test_cell_constructors(self):
        """
        Tests that the constructor for each different cell type runs
        successfully.
        """
        assert isinstance(self.mountain_cell, Mountain)
        assert isinstance(self.ocean_cell, Ocean)
        assert self.jungle_cell.parameters['f_max'] == 800.0
        assert isinstance(self.jungle_cell, Jungle)
        assert self.savannah_cell.parameters['f_max'] == 300.0
        assert self.savannah_cell.parameters['alpha'] == 0.3
        assert isinstance(self.savannah_cell, Savannah)
        assert isinstance(self.desert_cell, Desert)

    def test_sort_population(self):
        """
        Test that the sort_population static method sorts correctly based on
        the fitness of the animals. The first animal of the list shall have the
        highest fitness.
        """
        sorted_from_fitness = self.ocean_cell.sort_population(self.test_pop)
        assert sorted_from_fitness[0].fitness > sorted_from_fitness[1].fitness

    def test_calculate_relative_fodder(self):
        """
        Test that the calculate_relative_fodder static method calculates and
        returns the correct value for relative fodder.
        """
        relative_fodder = self.jungle_cell.calculate_relative_fodder(
            700,
            Herbivore,
            100
        )
        assert relative_fodder == (70 / 101)

    def test_nearby_relative_fodder(self):
        """
        Test that the nearby_relative_fodder method returns a list of tuples
        with correct values for relative_fodder in nearby_cells.
        """
        self.jungle_cell.population = [Herbivore()]
        animal = self.jungle_cell.population[0]

        nearby_1 = Ocean()
        nearby_2 = Jungle()
        nearby_3 = Jungle()
        nearby_4 = Savannah()

        nearby_2.population = [Herbivore() for _ in range(10)]
        nearby_4.population = [Herbivore() for _ in range(20)]

        self.jungle_cell.nearby_cells = [nearby_1,
                                         nearby_2,
                                         nearby_3,
                                         nearby_4]

        relative_fodder_list = self.jungle_cell.nearby_relative_fodder(animal)

        assert relative_fodder_list == [(0.0, nearby_1),
                                        (float(80/11), nearby_2),
                                        (80.0, nearby_3),
                                        (float(10/7), nearby_4)]

    def test_herbivores_in_cell(self):
        """
        Test if herbivores_in_cell property returns the correct value for
        the number of herbivores in the cell.
        """
        self.savannah_cell.population = self.test_pop
        assert self.savannah_cell.herbivores_in_cell == 3

    def test_carnivores_in_cell(self):
        """
        Test if carnivores_in_cell property returns the correct value for
        the number of carnivores in the cell.
        """
        self.desert_cell.population = self.test_pop
        assert self.desert_cell.carnivores_in_cell == 1

    def test_feeding_population_update(self):
        """
        Test if the feeding method updates the population correctly if at least
        one herbivore is eaten.
        """
        self.single_carn.get_fitness = 11
        self.jungle_cell.population = [Herbivore(),
                                       Herbivore(),
                                       Herbivore(),
                                       self.single_carn]
        self.jungle_cell.feeding()
        assert self.jungle_cell.herbivores_in_cell < 3

    def test_feeding_fodder_update(self):
        """
        Test that the fodder in the cell is updated correctly after one
        feeding.
        """
        self.jungle_cell.fodder = 500
        self.jungle_cell.population = [Herbivore() for _ in range(10)]
        Herbivore.parameters['F'] = 20
        self.jungle_cell.feeding()
        assert self.jungle_cell.fodder == 500 - 10 * 20

    def test_feeding_herbivores(self):
        """
        Tests that 'Herbivore.feed is called an expected number of times for
        herbivores in cell.
        """
        self.jungle_cell.population = self.herb_pop
        self.jungle_cell.feeding()
        assert self.mock_feed_herbivore.call_count == 4

    def test_feeding_carnivores(self):
        """
        Tests that 'Carnivore.kill is called an expected number of times for
        carnivores in cell.
        """
        self.jungle_cell.population = self.carn_pop
        self.jungle_cell.feeding()
        assert self.mock_feed_carnivore.call_count == 4

    def test_procreate(self):
        """
        Tests that 'Herbivore.gives_birth' is called an expected number of
        times for herbivores in cell.
        """
        self.jungle_cell.population = self.herb_pop
        self.jungle_cell.procreate()
        assert self.mock_procreate.call_count == 4

    def test_procreate_increases_pop_in_cell(self):
        """
        Tests that whenever an animal is born with by calling 'procreate', the
        newborn is added to the cell's population.
        """
        Herbivore().parameters['gamma'] = 20.0
        self.jungle_cell.population = self.herb_pop
        ini_cell_pop = len(self.jungle_cell.population)
        self.jungle_cell.procreate()
        assert len(self.jungle_cell.population) == ini_cell_pop + 4

        # Reset parameters
        Herbivore().parameters['gamma'] = 0.2

    def test_migration(self):
        """
        Tests that 'migration' is called an expected number of times for
        herbivores in cell.
        """
        self.jungle_cell.population = self.herb_pop
        self.jungle_cell.migration()
        assert self.mock_migrate.call_count == 4

    def test_aging(self):
        """
        Tests that 'aging' successfully increases the age of the
        animals in the cell's population. Also tests that the method
        Animals.loss_of_weight is called a correct number of times.
        """
        self.test_pop[0].get_fitness = 0
        self.jungle_cell.population = self.test_pop
        self.jungle_cell.aging()
        for animal in self.jungle_cell.population:
            assert animal.age == 3
        assert self.mock_aging.call_count == 4

    def test_loss_of_weight(self):
        """
        Tests that 'loss_of_weight' successfully adjusts the weight of the
        animals in the cell's population. Also tests that the method
        Animals.loss_of_weight is called a correct number of times.
        """
        self.test_pop[0].get_fitness = 0
        self.jungle_cell.population = self.test_pop
        self.jungle_cell.loss_of_weight()
        assert self.mock_loss_of_weight.call_count == 4

    def test_deaths(self):
        """
        Tests that 'deaths' successfully removes the animals from the cell's
        population. Also tests that the method Animals.death is called a
        correct number of times.
        """
        self.test_pop[0].get_fitness = 0
        self.jungle_cell.population = self.test_pop
        assert len(self.jungle_cell.population) == 4

        self.jungle_cell.deaths()
        assert len(self.jungle_cell.population) < 4
        assert self.mock_deaths.call_count == 4

    def test_fodder_growth(self):
        """
        Tests that 'fodder_growth' successfully replenishes the fodder in the
        cell as expected.
        """
        cells = [Jungle(), Savannah(), Desert()]

        assert cells[0].fodder == 800.0
        assert cells[1].fodder == 300.0
        assert cells[2].fodder == 0.0

        # Cell fodder is set to 0 then replenished
        for cell in cells:
            cell.fodder = 0.0
            cell.fodder_growth()

        assert cells[0].fodder == 800.0
        assert cells[1].fodder == 90.0
        assert cells[2].fodder == 0.0


class TestLandscapesTypes:
    """
    Tests for landscape types.
    """

    @pytest.fixture(autouse=True)
    def landscape_setup(self):
        """
        Setup for landscape type testing.
        """
        self.cell = Cell()
        self.ocean_cell = Ocean()
        self.jungle_cell = Jungle()
        self.savannah_cell = Savannah()
        self.mountain_cell = Mountain()
        self.desert_cell = Desert()

    def test_fodder_cell(self):
        """
        Testing if a default landscape cell has fodder = 0 when initializing
        the Cell class.
        """
        assert self.cell.fodder == 0

    def test_ocean_landscape(self):
        """
        Testing if a the Ocean subclass returns the correct string describing
        landscape_type.
        """
        assert self.ocean_cell.landscape_type == 'O'

    def test_ocean_fodder(self):
        """
        Testing if a the Ocean subclass returns the correct value for the
        amount of fodder in the cell.
        """
        assert self.ocean_cell.fodder == 0

    def test_mountain_landscape(self):
        """
        Testing if a the Mountain subclass returns the correct string
        describing landscape_type.
        """
        assert self.mountain_cell.landscape_type == 'M'

    def test_mountain_fodder(self):
        """
        Testing if a the Mountain subclass returns the correct value for the
        amount of fodder in the cell.
        """
        assert self.mountain_cell.fodder == 0

    def test_jungle_landscape(self):
        """
        Testing if a the Jungle subclass returns the correct string describing
        landscape_type.
        """
        assert self.jungle_cell.landscape_type == 'J'

    def test_jungle_fodder(self):
        """
        Testing if a the Jungle subclass returns the correct value for the
        amount of fodder in the cell right after initializing.
        """
        assert self.jungle_cell.fodder == self.jungle_cell.parameters['f_max']

    def test_savannah_landscape(self):
        """
        Testing if a the Savannah subclass returns the correct string
        describing landscape_type.
        """
        assert self.savannah_cell.landscape_type == 'S'

    def test_savannah_fodder(self):
        """
        Testing if a the Savannah subclass returns the correct value for the
        amount of fodder in the cell right after initializing.
        """
        assert self.savannah_cell.fodder == self.savannah_cell.parameters[
            'f_max'
        ]

    def test_desert_landscape(self):
        """
        Testing if a the Desert subclass returns the correct string describing
        landscape_type.
        """
        assert self.desert_cell.landscape_type == 'D'

    def test_desert_fodder(self):
        """
        Testing if a the Desert subclass returns the correct value for the
        amount of fodder in the cell.
        """
        assert self.desert_cell.fodder == 0
