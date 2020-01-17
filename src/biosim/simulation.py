# -*- coding: utf-8 -*-

"""
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import matplotlib.pyplot as plt
import textwrap
import pandas as pd
import numpy as np

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.cell import Ocean, Mountain, Jungle, Savannah, Desert
from src.biosim import cell

from src.biosim.island import Island


class BioSim:
    def __init__(
            self,
            island_map,
            ini_pop,
            seed,
            ymax_animals=None,
            cmax_animals=None,
            img_base=None,
            img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """

        self.island_map = island_map
        self.ini_pop = ini_pop
        self.seed = np.random.seed(seed)
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.image_base = img_base
        self.image_format = img_fmt

        self.years_simulated = 0

        self.simulated_island = Island(self.island_map)
        self.simulated_island.map_constructor()
        self.simulated_island.adding_population(self.ini_pop)
        self.simulated_island.generate_nearby_cells()

        self.figure = None
        self.map_axis = None
        self.mean_axis = None
        self.mean_line = None

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == 'Herbivore':
            for parameter in params:
                Herbivore.parameters[parameter] = params[parameter]
        elif species == 'Carnivore':
            for parameter in params:
                Carnivore.parameters[parameter] = params[parameter]
        else:
            raise ValueError

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'J':
            for parameter in params:
                Jungle.parameters[parameter] = params[parameter]
        elif landscape == 'S':
            for parameter in params:
                Savannah.parameters[parameter] = params[parameter]
        else:
            raise ValueError

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

        self.graphics_setup(num_years)

        for year in range(num_years):
            self.simulated_island.island_cycle()
            self.years_simulated += 1

            self.graphics_update()

        self.save_graphics()

    def graphics_setup(self, num_years):
        self.figure = plt.figure()

        self.map_axis = self.figure.add_subplot(1, 2, 1)

        self.mean_axis = self.figure.add_subplot(1, 2, 2)
        #self.mean_axis.set_ylim()

        self.mean_axis.set_xlim(0, num_years)

        mean_plot = self.mean_axis.plot(0, num_years)
        self.mean_line = mean_plot[0]

    def graphics_update(self):


        self.map_axis.plot(self.years_simulated, len(self.simulated_island.total_population()))


    def save_graphics(self):
        plt.savefig('test.png')

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

        self.simulated_island.adding_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self.years_simulated

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return len(self.simulated_island.total_population())

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        animals = self.simulated_island.total_population()
        number_of_herbivores = sum(isinstance(animal, Herbivore) for animal in animals)
        number_of_carnivores = sum(isinstance(animal, Carnivore) for animal in animals)
        return {"Herbivore": number_of_herbivores,
                "Carnivore": number_of_carnivores}

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

        island = self.simulated_island.island_map

        data = []

        for row in island:
            for cell in row:
                n_herbivores = cell.herbivores_in_cell
                n_carnivores = cell.carnivores_in_cell

                data.append([cell.coordinate[0], cell.coordinate[1], n_herbivores, n_carnivores])

        df = pd.DataFrame(data)
        df.columns = (["Row", "Col", "Herbivore", "Carnivore"])

        return df

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == '__main__':
    # Simulation with Herbivores and one single landscape cell,
    # a jungle cell in this case.

    #plt.ion()

    geogr = """\
               OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)

    sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    sim.set_animal_parameters(
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )
    sim.set_landscape_parameters("J", {"f_max": 700})

    sim.simulate(num_years=10, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_years=10, vis_years=1, img_years=2000)

    #plt.savefig("check_sim.pdf")

    #input("Press ENTER")

    # randvis_project for plotting

    # group lasso , sphinx, API Reference

    # do tox coverage, profiling

    # fixture, mocking, parameterize

    # profiling: %% prun