# -*- coding: utf-8 -*-

"""
Tests for simulation module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import textwrap
import pytest
import pandas as pd
from biosim.animals import Carnivore, Herbivore
from biosim.cell import Jungle, Savannah
from biosim.simulation import BioSim


class TestSimulation:
    """
    Tests for simulation.
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

        # Simulation
        sample_map = """\
                        JJOOOOJJJD
                        JJMMMJJDDD
                        DDDDDDDDDD"""
        sample_map = textwrap.dedent(sample_map)
        ini_pop = [
            {
                "loc": (2, 1),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)
                ],
            },
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(40)
                ],
            }
        ]

        self.sim = BioSim(sample_map, ini_pop, seed=123456)

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

        params_dict = {
            'omega': 0.9
        }

        # Tests for false string inputs
        with pytest.raises(ValueError):
            BioSim.set_animal_parameters(str(
                self.herbivore), params_dict
            )
            BioSim.set_animal_parameters(
                str(self.carnivore), params_dict
                    )

        params_tuple = [
            ('omega', 0.4)
        ]

        # Tests for bad dictionary format
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

        # Tests for false string inputs
        with pytest.raises(ValueError):
            BioSim.set_landscape_parameters(
                str(self.savannah_cell), params_dict
            )
            BioSim.set_landscape_parameters(
                str(self.jungle_cell), params_dict
            )

        # Tests for false dictionary formats
        with pytest.raises(TypeError):
            BioSim.set_landscape_parameters(
                self.str_savannah, params_tuple
            )
            BioSim.set_landscape_parameters(
                self.str_jungle, params_tuple
            )

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

    def test_carnivore_island_map(self):
        """
        Tests that the carnivore map is the same size as original island map.
        """
        carnivore_map = self.sim.carnivore_island_map()
        assert isinstance(carnivore_map, list)

    def test_herbivore_island_map(self):
        """
        Tests that the herbivore map is the same size as original island map.
        """
        herbivore_map = self.sim.herbivore_island_map()
        assert isinstance(herbivore_map, list)

    def test_add_population(self):
        """
        Tests that a population is successfully added to the island.
        The total number of animals should be the sum of initial population and
        the total number added.
        """
        population = [
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)
                ],
            },
            {
                "loc": (2, 2),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(40)
                ],
            }
        ]
        old_pop = self.sim.num_animals
        self.sim.add_population(population)
        assert self.sim.num_animals == 190 + old_pop
        assert self.sim.year == 0

    def test_year_property(self):
        """
        Tests that the correct year is returned.
        """
        self.sim.simulate(num_years=1)
        assert self.sim.year == 1

    def test_num_animals_property(self):
        """
        Tests that the correct number of animals is returned.
        """
        num_animals = self.sim.num_animals
        assert num_animals == 190
        assert self.sim.year == 0

    def test_num_animals_per_species(self):
        """
        Test that the correct number of animals per species is returned.
        """
        num_animals_per_species = self.sim.num_animals_per_species
        assert isinstance(num_animals_per_species, dict)
        assert num_animals_per_species['Herbivore'] == 150
        assert num_animals_per_species['Carnivore'] == 40
        assert self.sim.year == 0

    def test_animal_distribution(self):
        """
        Tests that 'animal_distribution' returns a DataFrame
        """
        data_frame = self.sim.animal_distribution
        assert isinstance(data_frame, pd.DataFrame)

    def test_make_movie(self):
        """
        Testing if a movie actually can be made.
        """
        self.sim._img_base = '../'
        self.sim.simulate(num_years=10, vis_years=1, img_years=5)
        _DEFAULT_MOVIE_FORMAT = 'mp4'
        self.sim.make_movie()

    def test_make_movies_raises_error(self):
        """
        Tests that 'make_movie' raises runtime error for no self._img_base.
        """
        with pytest.raises(RuntimeError):
            self.sim.make_movie()
