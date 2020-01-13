# -*- coding: utf-8 -*-

"""
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from src.biosim.animals import Herbivore, Carnivore
from src.biosim import cycle
import textwrap
import pandas as pd
from src.biosim.landscape import Ocean, Mountain, Jungle, Savannah, Desert
import numpy as np



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

        self.ini_pop = ini_pop
        self.seed = seed

        self.island_map = island_map.split('\n')

        for n in range(len(self.island_map)):
            self.island_map[n] = \
                [character for character in self.island_map[n]]

        self.landscape_dict = {'M': Mountain, 'O': Ocean, 'J': Jungle,
                          'S': Savannah, 'D': Desert}

        self.df = pd.DataFrame(index=range(len(self.island_map)),
                               columns=range(len(self.island_map[0])))

        for y in range(len(self.island_map)):
            for x in range(len(self.island_map[y])):
                self.df[x][y] = self.landscape_dict[self.island_map[y][x]]()

        for population in self.ini_pop:
            for animal in population['pop']:
                if animal['species'] == 'Herbivore':
                    self.df[population['loc'][0]][population['loc'][1]].population.append(
                        Herbivore(age=animal['age'], weight=animal['weight']))
                if animal['species'] == 'Carnivore':
                    self.df[population['loc'][0]][population['loc'][1]].population.append(
                        Carnivore(age=animal['age'], weight=animal['weight']))


    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        pass

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        pass

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

        # for year in range(num_years):
        #   for animal_object in self.df[self.x][self.y].population:
        #      cycle.annual_cycle(self.landscape_cell.population,
        #                        self.landscape_cell.fodder, animal_object,
        #                       n=len(self.df[self.x][self.y].population))

        # Have to run one part of cycle for each animal, not the total cycle
        # for one and one animal.

        for year in range(num_years):
            for index, row in self.df.iterrows():
                for cell in row:

                    for animal_object in cell.population:
                        nearby_herbivores = [animal for animal in cell.population if animal.__class__.__name__ == 'Herbivore']
                        cycle.feeding(animal_object, cell.fodder, nearby_herbivores)
                    for animal_object in cell.population:
                        cycle.procreate(cell.population, animal_object,
                                        n=len(cell.population)
                                        )
                    for animal_object in cell.population:
                        cycle.migrate(animal_object)
                    for animal_object in cell.population:
                        cycle.aging(animal_object)
                    for animal_object in cell.population:
                        cycle.loss_of_weight(animal_object)
                    for animal_object in cell.population:
                        cycle.death(cell.population, animal_object)

        return self.df

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == '__main__':
    # Simulation with Herbivores and one single landscape cell,
    # a jungle cell in this case.

    geogr = """\
               J"""
    map = textwrap.dedent(geogr)  # map = 'J'

    ini_pop = [
        {
            "loc": (0, 0),
            "pop": [
                {"species": "Herbivore", "age": 15, "weight": 40}
                for _ in range(100)
            ],
        },
        {
            "loc": (0, 0),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    simulation = BioSim(map, ini_pop, seed=1)

    cell_after_simulation = simulation.simulate(40)

    # This simulation runs fine now, just run the whole file and edit this
    # main block for testing.
    # Be careful with deleting and index changing in loops.
    # randvis_project for plotting

