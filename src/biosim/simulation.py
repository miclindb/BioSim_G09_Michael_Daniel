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

from biosim.animals import Herbivore, Carnivore
from biosim.cell import Ocean, Mountain, Jungle, Savannah, Desert
from biosim import cell
from biosim.island import Island

# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = '/users/michaellindberg/downloads/ffmpeg'
_CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'


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

        Parameters
        ----------
        island_map: str
            Multi-line string specifying island geography
        ini_pop: list
            List of dictionaries specifying initial population
        seed: int
            Integer used as random number seed
        ymax_animals: int
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals: dict
            Dict specifying color-code limits for animal densities
        img_base: str
            String with beginning of file name for figures, including path
        img_fmt: str
            String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

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
        self.herb_heat = None
        self.herb_heat_bar = None
        self.carn_heat = None
        self.carn_heat_bar = None
        self.title = None
        self.idx = 0
        self.xdata_herbs = None
        self.ydata_herbs = None

        self.xdata_carns = None
        self.ydata_carns = None

        self.counter_ax = None
        self.map_herb = None
        self.map_carn = None
        self.herb_count = None
        self.carn_count = None
        self.herb_txt = None
        self.carn_txt = None
        self.carn_template = None
        self.herb_template = None

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

            self.simulated_island.island_cycle()
            self.years_simulated += 1

            if self.year % vis_years == 0:
                self._update_graphics()

            if self.year % img_years == 0:
                self._save_graphics()

            self.idx += 1
            plt.pause(1e-6)

        self.idx = 0

    def _setup_graphics(self, num_years):
        """
        Graphical setup for visualization of the simulation.

        Parameters
        ----------
        num_years: int
            The number of years to be simulated.
        """

        self._img_base = '../BioSim_G09_Michael_Daniel/graphics/'

        if self._fig is None:
            self._fig = plt.figure(figsize=(20, 10))

        if self._ymax_animals is None:
            self._ymax_animals = 20000

        plt.title('')

        plt.axis('off')

        self._map_setup()
        self._graph_setup(num_years)
        self._carn_heat_map_setup()
        self._herb_heat_map_setup()
        self._herb_count_setup()
        self._carn_count_setup()

    def _map_setup(self):

        if self.map_ax is None:
            self.map_ax = self._fig.add_axes([0.02, 0.58, 0.45, 0.35])
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

            map_ax_lg = self._fig.add_axes([0.45, 0.7, 0.05, 0.3])
            map_ax_lg.axis('off')

            for idx, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                        'Savannah', 'Desert')):
                map_ax_lg.add_patch(plt.Rectangle((0.02, idx * 0.1), 0.3, 0.1,
                                             edgecolor='black',
                                             facecolor=rgb_values[name[0]]))
                map_ax_lg.text(0.4, idx * 0.1, name, transform=map_ax_lg.transAxes)

            self.map_ax.imshow(rgb_island_map, interpolation='nearest')
            self.map_ax.set_xticks(range(0, len(rgb_island_map[0]), 4))
            self.map_ax.set_xticklabels(range(1, 1 + len(rgb_island_map[0]), 4))
            self.map_ax.set_yticks(range(0, len(rgb_island_map), 4))
            self.map_ax.set_yticklabels(range(1, 1 + len(rgb_island_map), 4))

    def _graph_setup(self, num_years):
        """
        Setup for the graphs showing the number of herbivores and carnivores
        for the simulated year.

        Parameters
        ----------
        num_years: int
            The number of years to be simulated.

        """
        if self.ani_ax is not None:
            if self.idx == 0:
                self._fig.delaxes(self.ani_ax)

        if self.ani_ax is None or self.idx == 0:
            self.ani_ax = self._fig.add_axes([0.07, 0.07, 0.45, 0.4])

            plt.axis([0, num_years-1, 0, self._ymax_animals])

            self.title = plt.title('', weight='bold')

            self.xdata_herbs = np.arange(num_years)
            self.ydata_herbs = np.nan * np.ones(num_years)

            self.line_herbs = self.ani_ax.plot(self.xdata_herbs, self.ydata_herbs,
                                               'b-', label="Herbivores", linewidth=3.0)[0]

            self.xdata_carns = np.arange(num_years)
            self.ydata_carns = np.nan * np.ones(num_years)

            self.line_carns = self.ani_ax.plot(self.xdata_carns, self.ydata_carns,
                                               'r-', label='Carnivores', linewidth=3.0)[0]

            plt.grid()
            plt.legend(loc=1, prop={'size': 13})

        if self.year > 0:
            self.ani_ax.set_xticks(np.arange(num_years))
            self.ani_ax.set_xticklabels(
                np.arange(self.year + 1, num_years + self.year + 1))

        else:
            self.ani_ax.set_xticks(np.arange(0, num_years))
            self.ani_ax.set_xticklabels(np.arange(1, num_years + 1))

    def _herb_heat_map_setup(self):
        """
        Heat map setup for the herbivores.
        """
        if self.herb_heat is None:
            self.herb_heat = self._fig.add_axes([0.55, 0.65, 0.5, 0.3])
            plt.title("Herbivore distribution", weight='bold', fontsize=15)
            self.herb_heat.set_xticks(range(0, len(self.simulated_island.island_map[0]), 2))
            self.herb_heat.set_xticklabels(range(1, 1 + len(self.simulated_island.island_map[0]), 2))
            self.herb_heat.set_yticks(range(0, len(self.simulated_island.island_map), 2))
            self.herb_heat.set_yticklabels(range(1, 1 + len(self.simulated_island.island_map), 2))
            self.herb_heat_bar = plt.imshow([[0 for _ in range(21)] for _ in range(13)], cmap='jet', alpha=0.5, zorder=2)

            cbaxes = self._fig.add_axes([0.59, 0.65, 0.01, 0.3])
            plt.colorbar(self.herb_heat_bar, cax=cbaxes, orientation='vertical', ticks=[])

            self._herb_map_setup()

    def _carn_heat_map_setup(self):
        """
        Heat map setup for the carnivores.
        """
        if self.carn_heat is None:
            self.carn_heat = self._fig.add_axes([0.55, 0.10, 0.5, 0.3])
            plt.title("Carnivore distribution", weight='bold', fontsize=15)
            self.carn_heat.set_xticks(range(0, len(self.simulated_island.island_map[0]), 2))
            self.carn_heat.set_xticklabels(range(1, (1 + len(self.simulated_island.island_map[0])), 2))
            self.carn_heat.set_yticks(range(0, len(self.simulated_island.island_map), 2))
            self.carn_heat.set_yticklabels(range(1, (1 + len(self.simulated_island.island_map)), 2))
            self.carn_heat_bar = plt.imshow([[0 for _ in range(21)] for _ in range(13)], cmap='jet', alpha=0.5, zorder=2)

            cbaxes = self._fig.add_axes([0.59, 0.10, 0.01, 0.3])
            plt.colorbar(self.carn_heat_bar, cax=cbaxes, orientation='vertical', ticks=[])

            self._carn_map_setup()

    def _herb_map_setup(self):
        """
        Setup for the island map in the background of the herbivore heat map.
        """
        if self.map_herb is None:

            self.map_herb = self._fig.add_axes([0.55, 0.65, 0.5, 0.3])
            rgb_values = {
                "O": mcolors.to_rgba("cornflowerblue"),
                "J": mcolors.to_rgba("lightgreen"),
                "S": mcolors.to_rgba("linen"),
                "D": mcolors.to_rgba("lightyellow"),
                "M": mcolors.to_rgba("gainsboro"),
            }
            rgb_island_map = copy.deepcopy(self.simulated_island.island_map)
            rgb_island_map = [[rgb_values[cell.landscape_type] for cell in row]
                              for row in rgb_island_map]
            self.map_herb.imshow(rgb_island_map,
                                 interpolation='nearest',
                                 alpha=0.2,
                zorder=3
            )

    def _carn_map_setup(self):
        """
        Setup for the island map in the background of the carnivore heat map.
        """
        if self.map_carn is None:
            self.map_carn = self._fig.add_axes([0.55, 0.10, 0.5, 0.3])
            rgb_values = {
                "O": mcolors.to_rgba("cornflowerblue"),
                "J": mcolors.to_rgba("lightgreen"),
                "S": mcolors.to_rgba("linen"),
                "D": mcolors.to_rgba("lightyellow"),
                "M": mcolors.to_rgba("gainsboro"),
            }
            rgb_island_map = copy.deepcopy(self.simulated_island.island_map)
            rgb_island_map = [[rgb_values[cell.landscape_type] for cell in row]
                              for row in rgb_island_map]
            self.map_carn.imshow(
                rgb_island_map, interpolation='nearest', alpha=0.2, zorder=3
            )

    def _herb_count_setup(self):
        """
        Setup for the herbivore counter.
        """
        if self.herb_count is None:
            self.herb_count = self._fig.add_axes([0.70, 0.48, 0.2, 0.2])
            self.herb_count.axis('off')
            self.herb_template = 'Total number of herbivores: {:8}'
            self.herb_txt = self.herb_count.text(
                0.5, 0.5, self.herb_template.format(0),
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.herb_count.transAxes)
            self.herb_txt.set_text(self.herb_template.format(
                self.num_animals_per_species['Herbivore']))

    def _carn_count_setup(self):
        """
        Setup for the carnivore counter.
        """
        if self.carn_count is None:
            self.carn_count = self._fig.add_axes([0.70, 0.38, 0.2, 0.2])
            self.carn_count.axis('off')
            self.carn_template = 'Total number of carnivores: {:8}'
            self.carn_txt = self.carn_count.text(
                0.5, 0.5, self.carn_template.format(0),
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.carn_count.transAxes)
            self.carn_txt.set_text(self.carn_template.format(
                self.num_animals_per_species['Carnivore']))

    def _update_graphics(self):
        """
        Updating graphics in the figure (self._fig). This is run for each
        iteration in the simulation loop.
        """

        self._update_heat_map()
        self._update_graph()
        self._herb_count_update()
        self._carn_count_update()

    def _update_heat_map(self):
        """
        Updating the heat maps for herbivore and carnivore distribution.
        """
        self.herb_heat.imshow(
            self.herbivore_island_map(),
            interpolation='nearest',
            cmap='jet'
        )

        self.carn_heat.imshow(
            self.carnivore_island_map(),
            interpolation='nearest',
            cmap='jet'
        )

    def _update_graph(self):
        """
        Updating the graphs showing the number of carnivores and herbivores
        for each year in the simulation.
        """

        ydata_herbs = self.line_herbs.get_ydata()
        ydata_carns = self.line_carns.get_ydata()

        ydata_herbs[self.idx] = self.num_animals_per_species['Herbivore']
        ydata_carns[self.idx] = self.num_animals_per_species['Carnivore']

        self.line_herbs.set_ydata(ydata_herbs)
        self.line_carns.set_ydata(ydata_carns)

        self.title.set_text(
            'Year: {:5}'.format(self.years_simulated)
        )

    def _herb_count_update(self):
        """
        Updating the herbivore counter.
        """
        self.herb_txt.set_text(self.herb_template.format(
            self.num_animals_per_species['Herbivore']))

    def _carn_count_update(self):
        """
        Updating the carnivore counter.
        """
        self.carn_txt.set_text(self.carn_template.format(
            self.num_animals_per_species['Carnivore']))

    def _save_graphics(self):
        """
        Saving graphics.
        """

        if self._img_base is None:
            return

        plt.savefig(
            '{base}_{num:05d}.{type}'.format(
                base=self._img_base,
                num=self._img_ctr,
                type=self._img_fmt)
        )
        self._img_ctr += 1

    def add_population(self, population):
        """
        Adding a population to the island.

        Parameters
        ----------
        population: list
            List of dictionaries specifying population
        """

        self.simulated_island.adding_population(population)

    @property
    def year(self):
        """
        Last year simulated.
        """
        return self.years_simulated

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        return len(self.simulated_island.total_population())

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """

        animals = self.simulated_island.total_population()
        number_of_herbivores = sum(isinstance(animal, Herbivore) for animal in animals)
        number_of_carnivores = sum(isinstance(animal, Carnivore) for animal in animals)

        return {"Herbivore": number_of_herbivores,
                "Carnivore": number_of_carnivores}

    @property
    def animal_distribution(self):
        """
        Creating a pandas DataFrame with animal count per species for each
        cell on island.

        Returns
        -------
        df: pandas DataFrame
            The dataframe with animal counts per species for cell
            coordinates.
        """

        island = self.simulated_island.island_map

        data = []

        for row in island:
            for cell in row:
                n_herbivores = cell.herbivores_in_cell
                n_carnivores = cell.carnivores_in_cell

                data.append(
                    [cell.coordinate[0],
                     cell.coordinate[1],
                     n_herbivores,
                     n_carnivores])

        df = pd.DataFrame(data)
        df.columns = (["Row", "Col", "Herbivore", "Carnivore"])

        return df

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """

        movie_fmt = _DEFAULT_MOVIE_FORMAT

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError(
                    'ERROR: ffmpeg failed with: {}'.format(err)
                )


if __name__ == '__main__':

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

    #checksim, biosiminterface, code coverage, some visualization,

    # delivery: tag 'submission' in commit