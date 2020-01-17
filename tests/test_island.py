# -*- coding: utf-8 -*-
"""
Tests for island module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import textwrap
import pytest
import pytest_mock as pm
from src.biosim.island import Island
from src.biosim.cell import Cell, Ocean, Mountain, Jungle, Savannah, Desert
from src.biosim.animals import Animals, Herbivore, Carnivore


class TestIsland:

    def test_island_initializer(self):
        """
        Tests that the island initializer successfully initializes the island.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        JMMDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        assert island.island_map == sample_map
        assert len(island.landscape_dict) == 5

    def test_map_constructor(self):
        """
        Tests that the map constructor successfully constructs a list
        representing the map, and that the list's elements are class instances
        representing the landscape.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)

        island.map_constructor()
        assert len(island.island_map[0]) == 10
        assert len(island.island_map[1]) == 10
        assert len(island.island_map[2]) == 10
        assert isinstance(island.island_map, list)

        for element in island.island_map[2]:
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
        coordinates of the map. Tests that runs successfully for cells with
        less than four neighbouring cells.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()
        island.generate_nearby_cells()

        assert isinstance(island.island_map[0][0].nearby_cells, list)
        assert len(island.island_map[1][2].nearby_cells) == 4
        assert len(island.island_map[0][0].nearby_cells) == 2

        test_coordinates = island.island_map[-1][-2].nearby_cells
        assert len(island.island_map[-1][-2].nearby_cells) == 3
        assert isinstance(island.island_map[-1][-2].nearby_cells, list)

        for coordinate in test_coordinates:
            assert isinstance(coordinate, Desert)

    def test_adding_population(self):
        """
        Tests that the method successfully adds population to the desired
        coordinate.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

        test_population = [
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

        island.adding_population(test_population)
        pop_0 = island.island_map[0][0].population
        assert isinstance(pop_0, list)
        assert len(pop_0) == 2
        assert isinstance(pop_0[0], Herbivore)
        assert isinstance(pop_0[1], Carnivore)

        pop_1 = island.island_map[1][3].population
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
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

        test_population = [
            {
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Carnivore", "age": 1, "weight": 10.0},
                ],
            }
        ]

        with pytest.raises(ValueError):
            island.adding_population(test_population)

    def test_total_population_return(self):
        """
        Tests that the method returns correct list of total population on the
        island.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

        test_population = [
            {
                "loc": (0, 0),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                ],
            },
            {
                "loc": (1, 3),
                "pop": [
                    {"species": "Herbivore", "age": 15, "weight": 50.0},
                    {"species": "Herbivore", "age": 25, "weight": 20.0},
                    {"species": "Herbivore", "age": 2, "weight": 10.0}
                ],
            },
        ]

        island.adding_population(test_population)

        total_population = island.total_population()
        assert isinstance(total_population, list)
        assert len(total_population) == 5

        for animal in total_population:
            assert isinstance(animal, Herbivore)

    def test_island_fodder_growth(self):
        """
        Tests that the fodder is correct after calling 'island_fodder_growth'.
        """
        sample_map = """\
                        JDS"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

        assert island.island_map[0][0].fodder == 800.0
        assert island.island_map[0][1].fodder == 0.0
        assert island.island_map[0][2].fodder == 300.0

        island.island_map[0][0].fodder = 50.0
        island.island_map[0][1].fodder = 0.0
        island.island_map[0][2].fodder = 60.0

        island.island_fodder_growth()

        assert island.island_map[0][0].fodder == 800.0
        assert island.island_map[0][1].fodder == 0.0
        assert island.island_map[0][2].fodder == 132.0

    def test_island_growth_called_for_all_cells(self, mocker):
        mocker.spy(Cell, 'fodder')

        island.island_fodder_growth()


    def test_island_feeding(self):
        """
        Tests that feeding is successfully called.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

        island.island_feeding()

    def test_island_procreate(self):
        """
        Tests that procreate is successfully called.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

    def test_island_migration(self):
        """
        Tests that migration is successfully called.
        'has_moved' set to false.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

    def test_island_aging_calls(self, mocker):
        """
        Tests that aging is successfully called.
        """

        mocker.spy(Animals, 'age')

        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

        test_population = [
            {
                "loc": (0, 0),
                "pop": [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                ],
            }
        ]

        island.adding_population(test_population)

        island.aging()

        assert Island.island_aging.call_count == 2

    def test_island_loss_of_weight(self):
        """
        Tests that loss_of_weight is successfully called.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

    def test_island_deaths(self):
        """
        Tests that island_deaths is successfully called.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()

    def test_island_cycle(self):
        """
        Tests that island_cycle successfully calls expected methods.
        """
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        island = Island(sample_map)
        island.map_constructor()
