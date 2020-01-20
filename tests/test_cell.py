# -*- coding: utf-8 -*-
"""
A test for cell.py
"""

import pytest
from biosim.cell import Cell, Ocean, Mountain, Jungle, Savannah, Desert
from biosim.animals import Animals, Carnivore, Herbivore


class TestCellOperations:
    """
    Tests for operations in cell.
    """

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

        self.herb_pop = [Herbivore(age=2, weight=20),
                         Herbivore(age=2, weight=20),
                         Herbivore(age=2, weight=40),
                         Herbivore(age=2, weight=10)]

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
            700, Herbivore, 100
        )
        assert relative_fodder == (70 / 101)

    def test_nearby_relative_fodder(self):
        """
        Test that the nearby_relative_fodder method returns a list of tuples
        with correct values for relative_fodder in nearby_cells.
        """
        cell = Jungle()
        cell.population = [Herbivore()]
        animal = cell.population[0]

        nearby_1 = Ocean()
        nearby_2 = Jungle()
        nearby_3 = Jungle()
        nearby_4 = Savannah()

        nearby_2.population = [Herbivore() for _ in range(10)]
        nearby_4.population = [Herbivore() for _ in range(20)]

        cell.nearby_cells = [nearby_1, nearby_2, nearby_3, nearby_4]

        relative_fodder_list = cell.nearby_relative_fodder(animal)

        assert relative_fodder_list == [(0.0, nearby_1),
                                        (float(80/11), nearby_2),
                                        (80.0, nearby_3),
                                        (float(10/7), nearby_4)]

    def test_herbivores_in_cell(self):
        """
        Test if herbivores_in_cell property returns the correct value for
        the number of herbivores in the cell.
        """
        cell = Savannah()
        cell.population = [Carnivore(), Carnivore(), Herbivore(), Herbivore(),
                           Herbivore(), Herbivore()]

        assert cell.herbivores_in_cell == 4

    def test_carnivores_in_cell(self):
        """
        Test if carnivores_in_cell property returns the correct value for
        the number of carnivores in the cell.
        """
        cell = Desert()
        cell.population = [Carnivore(), Carnivore(), Herbivore(), Herbivore(),
                           Herbivore(), Herbivore()]

        assert cell.carnivores_in_cell == 2

    def test_feeding_population_update(self):
        """
        Test if the feeding method updates the population correctly if at least
        one herbivore is eaten.
        """
        cell = Jungle()
        carnivore = Carnivore()
        carnivore.get_fitness = 11

        cell.population = [Herbivore(), Herbivore(), Herbivore(), carnivore]
        cell.feeding()

        assert cell.herbivores_in_cell < 3

    def test_feeding_fodder_update(self):
        """
        Test that the fodder in the cell is updated correctly after one
        feeding.
        """
        cell = Jungle()
        cell.fodder = 500

        cell.population = [Herbivore() for _ in range(10)]
        Herbivore.parameters['F'] = 20

        cell.feeding()

        assert cell.fodder == 500 - 10 * 20

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
        cells = [self.jungle_cell, self.savannah_cell, self.desert_cell]

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
            'f_max']

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
