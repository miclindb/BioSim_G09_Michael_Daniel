# -*- coding: utf-8 -*-

"""
Tests for simulation module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import textwrap

import pytest
from biosim import Island, BioSim, Jungle, Savannah, Carnivore, Herbivore
from biosim.animals import Carnivore, Herbivore
from biosim.cell import Jungle, Savannah
from biosim.island import Island
from biosim.simulation import BioSim


class TestSimulation:
    """
    Tests for simulation.
    """

    @pytest.fixture(autouse=True)
    def setup_simulation(self):
        """
        Setup for simulation tests.
        """
        # Animals
        self.herbivore = Herbivore()
        self.str_herbivore = 'Herbivore'
        self.carnivore = Carnivore()
        self.str_carnivore = 'Carnivore'

        # Landscape cells
        self.jungle_cell = Jungle()
        self.str_jungle = 'J'
        self.savannah_cell = Savannah()
        self.str_savannah = 'S'

        # Island map
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        self.sample_map = textwrap.dedent(sample_map)
        self.simulated_island_map = Island(self.sample_map)

    def test_animal_parameter(self):
        """
        Test that the parameters of the animals are correct after they are
        changed.
        """
        assert self.herbivore.parameters['omega'] == 0.4
        assert self.carnivore.parameters['omega'] == 0.9
        params = {
            'omega': 0.4
        }
        BioSim.set_animal_parameters(self.str_herbivore, params)
        BioSim.set_animal_parameters(self.str_carnivore, params)

        # Checks that correct parameter is changed
        assert self.herbivore.parameters['omega'] == 0.4
        assert self.herbivore.parameters['eta'] == 0.05
        assert self.carnivore.parameters['omega'] == 0.4
        assert self.carnivore.parameters['eta'] == 0.125

    def test_animal_parameter_raises_error(self):
        """
        Tests changing animal parameters raises ValueError for bad input.
        """

        assert self.herbivore.parameters['omega'] == 0.4
        assert self.carnivore.parameters['omega'] == 0.4
        params_dict = {
            'omega': 0.9
        }
        # Tests for non-string inputs
        with pytest.raises(ValueError):
            BioSim.set_animal_parameters(Herbivore, params_dict)
            BioSim.set_animal_parameters(Carnivore, params_dict)

        params_tuple = [
            ('omega', 0.4)
        ]
        # Tests for bad parameters format
        with pytest.raises(TypeError):
            BioSim.set_animal_parameters(self.str_herbivore, params_tuple)
            BioSim.set_animal_parameters(self.str_carnivore, params_tuple)

        # Reset carnivore parameters
        BioSim.set_animal_parameters(self.str_carnivore, params_dict)
        assert self.herbivore.parameters['omega'] == 0.4
        assert self.carnivore.parameters['omega'] == 0.9

    def test_set_landscape_parameter(self):
        """
        Test that the parameters of the landscape are correct after they are
        changed. Also tests new parameters are added when they don't already
        exist.
        """
        params = {
            'f_max': 100.0,
            'alpha': 0.2
        }
        BioSim.set_landscape_parameters(self.str_savannah, params)
        BioSim.set_landscape_parameters(self.str_jungle, params)
        assert self.savannah_cell.parameters['f_max'] == 100.0
        assert self.savannah_cell.parameters['alpha'] == 0.2
        assert self.jungle_cell.parameters['f_max'] == 100.0
        assert self.jungle_cell.parameters['alpha'] == 0.2

    def test_landscape_parameter_raises_error(self):
        """
        Tests changing landscape parameters raises ValueError for bad input.
        """
        params_dict = {
            'f_max': 100.0,
            'alpha': 0.2
        }
        params_tuple = [
            ('f_max', 100.0),
            ('alpha', 0.2)
        ]

        # Tests for non-string inputs
        with pytest.raises(ValueError):
            BioSim.set_landscape_parameters(self.savannah_cell, params_dict)
            BioSim.set_landscape_parameters(self.jungle_cell, params_dict)

        # Tests for bad parameters format
        with pytest.raises(TypeError):
            BioSim.set_landscape_parameters(self.str_savannah, params_tuple)
            BioSim.set_landscape_parameters(self.str_jungle, params_tuple)

        # Reset landscape parameters
        params_s = {
            'f_max': 300.0,
            'alpha': 0.3
        }
        params_j = {
            'f_max': 800.0
        }
        BioSim.set_landscape_parameters(self.str_savannah, params_s)
        BioSim.set_landscape_parameters(self.str_jungle, params_j)

        assert self.savannah_cell.parameters['f_max'] == 300.0
        assert self.savannah_cell.parameters['alpha'] == 0.3
        assert self.jungle_cell.parameters['f_max'] == 800.0
        assert self.jungle_cell.parameters['alpha'] == 0.2

    def test_carnivore_island_map(self):
        """
        Tests that the carnivore map is the same size as original island map.
        """
        self.simulated_island.map_constructor()
        carnivore_map = x
        assert isinstance(carnivore_map, list)
        assert len(carnivore_map[0]) == len(self.island_map[0])

    def test_herbivore_island_map(self):
        """
        Tests that the herbivore map is the same size as original island map.
        """
        self.simulated_island.map_constructor()

    def test_simulate(self):
        """

        """

    def test_setup_graphics(self):
        """

        """

    def test_herb_count_setup(self):
        """

        """

    def test_carn_count_setup(self):
        """

        """

    def test_map_setup(self):
        """

        """

    def test_graph_setup(self):
        """

        """

    def test_herb_heat_map_setup(self):
        """

        """

    def test_carn_heat_map_setup(self):
        """

        """

    def test_herb_map_setup(self):
        """

        """

    def test_can_map_setup(self):
        """

        """

    def test_herb_count_setup(self):
        """

        """

    def test_carn_count_setup(self):
        """

        """

    def test_update_graphics(self):
        """

        """

    def test_update_heat_map(self):
        """

        """

    def test_update_graphs(self):
        """

        """

    def test_herb_count_update(self):
        """

        """

    def test_carn_count_update(self):
        """

        """

    def test_save_graphics(self):
        """

        """

    def test_add_population(self):
        """
        Tests that a population is successfully added to the island.
        """

    def test_year_property(self):
        """
        Tests that the correct year is returned.
        """

    def test_num_animals_property(self):
        """

        """

    def test_num_animals_per_species(self):
        """
        Test that the correct number of animals per species is returned.
        """

    def test_animal_distribution(self):
        """

        """

    def test_make_movie(self):
        """

        """
