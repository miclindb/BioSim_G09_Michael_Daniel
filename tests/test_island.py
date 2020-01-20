# -*- coding: utf-8 -*-

"""
Tests for island module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import textwrap
import pytest
from biosim.island import Island
from biosim.cell import Cell, Desert
from biosim.animals import Herbivore, Carnivore


class TestIsland:
    """
    Tests for island operations.
    """

    @pytest.fixture(autouse=True)
    def setup_island(self):
        """
        Setup for island tests.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        self.sample_map = textwrap.dedent(sample_map)
        self.island = Island(self.sample_map)
        self.test_population = [
            {
                "loc": (0, 0),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            },
            {
                "loc": (1, 3),
                "pop": [
                    {"species": "Carnivore", "age": 15, "weight": 50.0},
                    {"species": "Herbivore", "age": 25, "weight": 20.0},
                    {"species": "Herbivore", "age": 2, "weight": 10.0}
                ],
            },
        ]
        self.bad_population_input = [
            {
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            }
        ]
        self.herbivore_population = [
            {
                "loc": (1, 3),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(5)
                ],
            }
        ]
        self.carnivore_population = [
            {
                "loc": (1, 3),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(5)
                ],
            }
        ]

    def test_island_initializer(self):
        """
        Tests that the island initializer successfully initializes the island.
        """
        assert self.island.island_map == self.sample_map
        assert len(self.island.landscape_dict) == 5

    def test_map_constructor(self):
        """
        Tests that the map constructor successfully constructs a list
        representing the map, and that the list's elements are class instances
        representing the landscape.
        """
        self.island.map_constructor()
        assert len(self.island.island_map[0]) == 10
        assert len(self.island.island_map[1]) == 10
        assert len(self.island.island_map[2]) == 10
        assert isinstance(self.island.island_map, list)

        for element in self.island.island_map[2]:
            assert isinstance(element, Desert)

    def test_uneven_map_raises_error_in_constructor(self):
        """
        Tests that the map constructor successfully raises ValueError when it
        gets an invalid input map.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        with pytest.raises(ValueError):
            island.map_constructor()

        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD
                        M"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        with pytest.raises(ValueError):
            island.map_constructor()

        sample_map = """\
                        
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        with pytest.raises(ValueError):
            island.map_constructor()

    def test_generate_nearby_cells(self):
        """
        Tests that the method successfully generates a list of nearby cells for
        coordinates of the map. Also tests that runs successfully for cells
        with less than four neighbouring cells.
        """
        self.island.map_constructor()
        self.island.generate_nearby_cells()

        assert isinstance(self.island.island_map[0][0].nearby_cells, list)
        assert len(self.island.island_map[1][2].nearby_cells) == 4
        assert len(self.island.island_map[0][0].nearby_cells) == 2

        test_coordinates = self.island.island_map[-1][-2].nearby_cells
        assert len(self.island.island_map[-1][-2].nearby_cells) == 3
        assert isinstance(self.island.island_map[-1][-2].nearby_cells, list)

        for coordinate in test_coordinates:
            assert isinstance(coordinate, Desert)

    def test_add_herbivores(self):
        """
        Tests that herbivores can successfully be added to the island.
        """
        self.island.map_constructor()
        self.island.adding_population(self.herbivore_population)

        pop_herb = self.island.island_map[1][3].population
        assert isinstance(pop_herb, list)
        assert len(pop_herb) == 5
        assert isinstance(pop_herb[0], Herbivore)

    def test_add_carnivores(self):
        """
        Tests that carnivores can successfully be added to the island.
        """
        self.island.map_constructor()
        self.island.adding_population(self.carnivore_population)

        pop_carn = self.island.island_map[1][3].population
        assert isinstance(pop_carn, list)
        assert len(pop_carn) == 5
        assert isinstance(pop_carn[0], Carnivore)

    def test_adding_population(self):
        """
        Tests that the method successfully adds population to the desired
        coordinate.
        """
        self.island.map_constructor()
        self.island.adding_population(self.test_population)

        pop_0 = self.island.island_map[0][0].population
        assert isinstance(pop_0, list)
        assert len(pop_0) == 2
        assert isinstance(pop_0[0], Herbivore)
        assert isinstance(pop_0[1], Carnivore)

        pop_1 = self.island.island_map[1][3].population
        assert isinstance(pop_1, list)
        assert len(pop_1) == 3
        assert isinstance(pop_1[0], Carnivore)
        assert isinstance(pop_1[1], Herbivore)
        assert isinstance(pop_1[2], Herbivore)

    def test_adding_population_bad_input(self):
        """
        Tests that adding_population raises ValueError whenever a bad input is
        given.
        """
        self.island.map_constructor()
        with pytest.raises(ValueError):
            self.island.adding_population(self.bad_population_input)

    def test_total_population_return(self):
        """
        Tests that the method returns correct list of total population on the
        island.
        """
        self.island.map_constructor()
        self.island.adding_population(self.herbivore_population)

        total_population = self.island.total_population()
        assert isinstance(total_population, list)
        assert len(total_population) == 5

        for animal in total_population:
            assert isinstance(animal, Herbivore)


class TestIslandCycles:
    """
    Tests for island cycles.
    """

    @pytest.fixture(autouse=True)
    def setup_island(self, mocker):
        """
        Setup for island cycles testing.
        """
        small_sample_map = """\
                            JDS"""
        self.small_sample_map = textwrap.dedent(small_sample_map)
        self.small_island = Island(self.small_sample_map)
        self.sample_map = """\
                            JJOOOOJJJD
                            JJMMMJJDDD
                            DDDDDDDDDD"""
        self.sample_map = textwrap.dedent(self.sample_map)
        self.sample_map_length = len(self.sample_map)
        self.island = Island(self.sample_map)
        self.test_population = [
            {
                "loc": (0, 0),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                ],
            }
        ]

        # Setup for mocking
        self.mock_fodder_growth = mocker.spy(Cell, 'fodder_growth')
        self.mock_feeding = mocker.spy(Cell, 'feeding')
        self.mock_procreate = mocker.spy(Cell, 'procreate')
        self.mock_migration = mocker.spy(Cell, 'migration')
        self.mock_aging = mocker.spy(Cell, 'aging')
        self.mock_loss_of_weight = mocker.spy(Cell, 'loss_of_weight')
        self.mock_deaths = mocker.spy(Cell, 'deaths')

    def test_island_fodder_growth(self):
        """
        Tests that the fodder is correct after calling 'island_fodder_growth'.
        """
        self.small_island.map_constructor()

        assert self.small_island.island_map[0][0].fodder == 800.0
        assert self.small_island.island_map[0][1].fodder == 0.0
        assert self.small_island.island_map[0][2].fodder == 300.0

        self.small_island.island_map[0][0].fodder = 50.0
        self.small_island.island_map[0][1].fodder = 0.0
        self.small_island.island_map[0][2].fodder = 60.0

        self.small_island.island_fodder_growth()

        assert self.small_island.island_map[0][0].fodder == 800.0
        assert self.small_island.island_map[0][1].fodder == 0.0
        assert self.small_island.island_map[0][2].fodder == 132.0

    def test_island_growth_called_for_all_cells(self):
        """
        Tests that fodder growth is called for all cells.
        """
        self.island.map_constructor()
        self.island.island_fodder_growth()
        assert self.mock_fodder_growth.call_count == 30

    def test_island_feeding(self):
        """
        Tests that feeding is successfully called for all cells.
        """
        self.island.map_constructor()
        self.island.island_feeding()
        assert self.mock_feeding.call_count == 30

    def test_island_procreate(self):
        """
        Tests that procreate is successfully called for all cells.
        """
        self.island.map_constructor()
        self.island.island_procreate()
        assert self.mock_procreate.call_count == 30

    def test_island_migration(self):
        """
        Tests that migration has been successfully called for all cells.
        """
        self.island.map_constructor()
        self.island.island_migration()
        assert self.mock_migration.call_count == 30

    def test_island_aging_calls(self):
        """
        Tests that aging is successfully called for all cells.
        """
        self.island.map_constructor()
        self.island.adding_population(self.test_population)
        self.island.island_aging()
        assert self.mock_aging.call_count == 30

    def test_island_loss_of_weight(self):
        """
        Tests that loss_of_weight is successfully called for all cells.
        """
        self.island.map_constructor()
        self.island.island_loss_of_weight()
        assert self.mock_loss_of_weight.call_count == 30

    def test_island_deaths(self):
        """
        Tests that island_deaths is successfully called for all cells.
        """
        self.island.map_constructor()
        self.island.island_deaths()
        assert self.mock_deaths.call_count == 30

    def test_island_cycle(self):
        """
        Tests that island_cycle successfully calls expected methods an expected
        number of times.
        """
        self.island.map_constructor()
        self.island.adding_population(self.test_population)
        self.island.island_cycle()
        assert self.mock_fodder_growth.call_count == 30
        assert self.mock_feeding.call_count == 30
        assert self.mock_procreate.call_count == 30
        assert self.mock_migration.call_count == 30
        assert self.mock_aging.call_count == 30
        assert self.mock_loss_of_weight.call_count == 30
        assert self.mock_deaths.call_count == 30
