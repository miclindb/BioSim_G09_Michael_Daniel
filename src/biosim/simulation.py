# -*- coding: utf-8 -*-

"""
Simulation Module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import textwrap
import pandas as pd
import numpy as np
import subprocess
import copy
import os

from src.biosim.animals import Herbivore, Carnivore
from src.biosim.cell import Ocean, Mountain, Jungle, Savannah, Desert
from src.biosim import cell
from src.biosim.island import Island

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'   # alternatives: mp4, gif


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
        self._ymax_animals = ymax_animals
        self._cmax_animals = cmax_animals
        self._img_fmt = img_fmt
        self._img_base = img_base

        self.years_simulated = 0

        self.simulated_island = Island(self.island_map)
        self.simulated_island.map_constructor()
        self.simulated_island.adding_population(self.ini_pop)
        self.simulated_island.generate_nearby_cells()

        self._img_dir = None

        if self._img_dir is not None:
            self._img_base = os.path.join(self._img_dir, img_name)
        else:
            self._img_base = None

        self._final_year = None
        self._img_ctr = 0

        # following will be initialized by _setup_graphics
        self._fig = None

        self.line_carns = None
        self.line_herbs = None

        self.map_ax = None
        self.ani_ax = None
        self.ax3 = None
        self.ax3_bar = None
        self.ax4 = None
        self.ax4_bar = None
        self.title = None
        self.idx = 0
        self.xdata_herbs = None
        self.ydata_herbs = None

        self.xdata_carns = None
        self.ydata_carns = None

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

    def carnivore_island_map(self):
        carnivore_map = copy.deepcopy(self.simulated_island.island_map)
        carnivore_map = [[cell.carnivores_in_cell for cell in row] for row in carnivore_map]
        return carnivore_map

    def herbivore_island_map(self):
        herbivore_map = copy.deepcopy(self.simulated_island.island_map)
        herbivore_map = [[cell.herbivores_in_cell for cell in row] for row in herbivore_map]
        return herbivore_map

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

        plt.ion()

        if img_years is None:
            img_years = vis_years

        self._setup_graphics(num_years)

        for _ in range(num_years):

            if self.year % vis_years == 0:
                self._update_graphics()

            if self.year % img_years == 0:
                self._save_graphics()

            self.simulated_island.island_cycle()

            self.years_simulated += 1
            self.idx += 1

        self.idx = 0

    def _setup_graphics(self, num_years):
        """Creates subplots."""

        self._fig = plt.figure(figsize=(20, 10))

        if self._ymax_animals is None:
            self._ymax_animals = 20000

        plt.title('')

        plt.axis('off')

        self._fig.set_tight_layout(True)

        ###################### MAP ########################
        self.map_ax = self._fig.add_subplot(2, 2, 1)
        plt.title('Island map', weight='bold', fontsize=20)

        rgb_values = {
            "O": mcolors.to_rgba("navy"),
            "J": mcolors.to_rgba("darkgreen"),
            "S": mcolors.to_rgba("#e1ab62"),
            "D": mcolors.to_rgba("palegoldenrod"),
            "M": mcolors.to_rgba("dimgray"),
        }

        rgb_island_map = copy.deepcopy(self.simulated_island.island_map)

        rgb_island_map = [[rgb_values[cell.landscape_type] for cell in row]
                          for row in rgb_island_map]

        map_ax_lg = self._fig.add_axes([0.02, 0.65, 0.05, 0.5])
        map_ax_lg.axis('off')

        for idx, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                    'Savannah', 'Desert')):
            map_ax_lg.add_patch(plt.Rectangle((0., idx * 0.1), 0.3, 0.1,
                                         edgecolor='black',
                                         facecolor=rgb_values[name[0]]))
            map_ax_lg.text(0.4, idx * 0.1, name, transform=map_ax_lg.transAxes)

        self.map_ax.imshow(rgb_island_map, interpolation='nearest')
        self.map_ax.set_xticks(range(0, len(rgb_island_map[0]), 4))
        self.map_ax.set_xticklabels(range(1, 1 + len(rgb_island_map[0]), 4))
        self.map_ax.set_yticks(range(0, len(rgb_island_map), 4))
        self.map_ax.set_yticklabels(range(1, 1 + len(rgb_island_map), 4))

        self.ani_ax = self._fig.add_subplot(2, 2, 3)

        plt.axis([0, num_years, 0, self._ymax_animals])

        self.title = plt.title('')

        self.xdata_herbs = np.arange(num_years+1)
        self.ydata_herbs = np.nan * np.ones(num_years+1)

        self.line_herbs = self.ani_ax.plot(self.xdata_herbs, self.ydata_herbs,
                                        'g-', label="Herbivores")[0]

        self.xdata_carns = np.arange(num_years+1)
        self.ydata_carns = np.nan * np.ones(num_years+1)

        self.line_carns = self.ani_ax.plot(self.xdata_carns, self.ydata_carns,
                                        'r-', label='Carnivores')[0]

        #if self.year > 0:
        #    self.ani_ax.set_xticklabels(np.arange(num_years))
        #
        #else:
        self.ani_ax.set_xticks(np.arange(num_years))
        self.ani_ax.set_xticklabels(np.arange(num_years))

        plt.grid()
        plt.legend(loc=1, prop={'size': 7})


        self.ax3 = self._fig.add_subplot(2, 2, 2)
        plt.title("Herbivore distribution", weight='bold', fontsize=15)
        self.ax3.set_xticks(range(0, len(self.simulated_island.island_map[0]), 2))
        self.ax3.set_xticklabels(range(1, 1 + len(self.simulated_island.island_map[0]), 2))
        self.ax3.set_yticks(range(0, len(self.simulated_island.island_map), 2))
        self.ax3.set_yticklabels(range(1, 1 + len(self.simulated_island.island_map), 2))
        self.ax3_bar = plt.imshow([[0 for _ in range(21)] for _ in range(13)])


        self.ax4 = self._fig.add_subplot(2, 2, 4)
        plt.title("Carnivore distribution", weight='bold', fontsize=15)
        self.ax4.set_xticks(range(0, len(self.simulated_island.island_map[0]), 2))
        self.ax4.set_xticklabels(range(1, (1 + len(self.simulated_island.island_map[0])), 2))
        self.ax4.set_yticks(range(0, len(self.simulated_island.island_map), 2))
        self.ax4.set_yticklabels(range(1, (1 + len(self.simulated_island.island_map)), 2))
        self.ax4_bar = plt.imshow([[0 for _ in range(21)] for _ in range(13)])

    def _update_graphics(self):

        self.ax3.imshow(self.herbivore_island_map(), interpolation='nearest',
                   cmap='jet')

        self.ax4.imshow(self.carnivore_island_map(), interpolation='nearest',
                   cmap='jet')

        ydata_herbs = self.line_herbs.get_ydata()
        ydata_carns = self.line_carns.get_ydata()

        ydata_herbs[self.idx] = self.num_animals_per_species['Herbivore']
        ydata_carns[self.idx] = self.num_animals_per_species['Carnivore']

        self.line_herbs.set_ydata(ydata_herbs)
        self.line_carns.set_ydata(ydata_carns)

        self.title.set_text('Year: {:5}'.format(self.years_simulated))

    def _save_graphics(self):

        #if self._img_base is None:
         #   return
        plt.savefig('{num}.png'.format(num=self._img_ctr))

        #plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
          #                                           num=self._img_ctr,
           #                                          type=self._img_fmt))
        self._img_ctr += 1

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

        """
        Creates MPEG4 movie from visualization images saved.
        .. :note:
            Requires ffmpeg
        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)


if __name__ == '__main__':
    # Simulation with Herbivores and one single landscape cell,
    # a jungle cell in this case.

    plt.ion()

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

    sim.simulate(num_years=10, vis_years=1, img_years=5)

    sim.add_population(population=ini_carns)

    sim.simulate(num_years=10, vis_years=1, img_years=5)

    plt.savefig("check_sim.pdf")

    #input("Press ENTER")

    # randvis_project for plotting

    # group lasso , sphinx, API Reference

    # do tox coverage, profiling

    # fixture, mocking, parameterize

    # profiling: %% prun
