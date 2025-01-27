# -*- coding: utf-8 -*-

"""
Island Module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from .cell import Ocean, Mountain, Jungle, Savannah, Desert
from .animals import Herbivore, Carnivore


class Island:
    """
    Island class. Superclass for all landscape types.
    """

    def __init__(self, island_map):
        """
        Class constructor for island.

        Parameters
        ----------
        island_map: str
            String containing information about the island such as shape and
            landscape type.
        """
        self.island_map = island_map
        self.landscape_dict = {'M': Mountain,
                               'O': Ocean,
                               'J': Jungle,
                               'S': Savannah,
                               'D': Desert}

    def construct_vertical_coordinates(self, h_axis):
        """
        Constructs the vertical coordinates for the island map.
        """
        for x in range(len(self.island_map[h_axis])):
            if self.island_map[h_axis][x] not in self.landscape_dict.keys():
                raise ValueError('Landscape type does not exist')
            else:
                self.island_map[h_axis][x] = self.landscape_dict[
                    self.island_map[h_axis][x]
                ]()
                self.island_map[h_axis][x].coordinate = (h_axis, x)

    def construct_map_coordinates(self):
        """
        Construct the coordinates of the island map.
        """
        for y in range(len(self.island_map)):
            iteration = iter(self.island_map)
            length = len(next(iteration))
            if not all(len(list) == length for list in iteration):
                raise ValueError('Inconsistent line length')
            if self.island_map[y][0] != 'O' and self.island_map[y][1] == 'O':
                print(self.island_map[y][0], self.island_map[y][1])
                raise ValueError('Bad boundary')

            self.construct_vertical_coordinates(h_axis=y)

    def map_constructor(self):
        """
        Constructs the entire map of the island.
        """
        self.island_map = self.island_map.split('\n')

        for n in range(len(self.island_map)):
            self.island_map[n] = \
                [character for character in self.island_map[n]]

        self.construct_map_coordinates()

    def generate_cell_above(self, x, y, list_of_nearby_cells):
        """
        Generates cell above current cell.
        """
        cell_1 = self.island_map[y - 1][x]
        list_of_nearby_cells.append(cell_1)

    def generate_cell_left(self, x, y, list_of_nearby_cells):
        """
        Generates cell to the left of current cell.
        """
        cell_2 = self.island_map[y][x - 1]
        list_of_nearby_cells.append(cell_2)

    def generate_cell_below(self, x, y, list_of_nearby_cells):
        """
        Generates cell below current cell.
        """
        cell_3 = self.island_map[y + 1][x]
        list_of_nearby_cells.append(cell_3)

    def generate_cell_right(self, x, y, list_of_nearby_cells):
        """
        Generates cell to the right of current cell.
        """
        cell_4 = self.island_map[y][x + 1]
        list_of_nearby_cells.append(cell_4)

    def generate_nearby_cells(self):
        """
        Generates a list of cells near current cell. These cells are used for
        animal migration.
        """
        for y in range(len(self.island_map)):
            for x in range(len(self.island_map[y])):
                list_of_nearby_cells = []

                if y != 0:
                    self.generate_cell_above(x, y, list_of_nearby_cells)

                if x != 0:
                    self.generate_cell_left(x, y, list_of_nearby_cells)

                if y != len(self.island_map)-1:
                    self.generate_cell_below(x, y, list_of_nearby_cells)

                if x != len(self.island_map[y])-1:
                    self.generate_cell_right(x, y, list_of_nearby_cells)

                self.island_map[y][x].nearby_cells = list_of_nearby_cells

    def add_herbivores(self, animal, animal_list):
        """
        Adds herbivores to the island population. Used for 'adding_population'
        method.

        Parameters
        ----------
        animal: Herbivore
            Herbivore object to be added to the population.
        animal_list: list
            List of animals to be added to the population.
        """
        self.island_map[animal_list['loc'][0]][
            animal_list['loc'][1]].population.append(
            Herbivore(age=animal['age'], weight=animal['weight']))

    def add_carnivores(self, animal, animal_list):
        """
        Adds carnivores to the island population. Used for 'adding_population'
        method.

        Parameters
        ----------
        animal: Carnivore
            Carnivore object to be added to the population.
        animal_list: list
            List of animals to be added to the population.
        """
        self.island_map[animal_list['loc'][0]][
            animal_list['loc'][1]].population.append(
            Carnivore(age=animal['age'], weight=animal['weight']))

    def adding_population(self, population):
        """
        Adds population to the island.

        Parameters
        ----------
        population: List
            List containing dictionaries describing the population's location
            and population type.

            Required format:
            ini_animals = [{
            "loc": (coordinate_x, coordinate_y),
            "pop": [
                {"species": str(animal_species), "age": age, "weight": weight}
                for _ in range(number_of_animals)
                ],
            }]
        """
        try:
            for animals in population:
                for animal in animals['pop']:
                    if animal['species'] == 'Herbivore':
                        self.add_herbivores(animal, animals)
                    if animal['species'] == 'Carnivore':
                        self.add_carnivores(animal, animals)
        except (ValueError, KeyError):
            raise ValueError(
                'Invalid input for population, see documentation.'
            )

    def total_population(self):
        """
        Constructs a list containing all the animals on the island.

        Returns
        -------
        total_population_list: list
            List containing the total population on the island.
        """
        total_population_list = []
        for y in self.island_map:
            for cell in y:
                total_population_list += cell.population
        return total_population_list

    def island_fodder_growth(self):
        """
        Yearly cycle for fodder growth. Fodder grows for all cells on the
        island.
        """
        for y in self.island_map:
            for cell in y:
                cell.fodder_growth()

    def island_feeding(self):
        """
        Yearly cycle for feeding. All animals on the island attempts to feed.
        """
        for y in self.island_map:
            for cell in y:
                cell.feeding()

    def island_procreate(self):
        """
        Yearly cycle for procreation. All animals on the island attempts to
        procreate.
        """
        for y in self.island_map:
            for cell in y:
                cell.procreate()

    def island_migration(self):
        """
        Yearly cycle for migration. All animals on the island cell attempts to
        migrate. Resets the 'has_moved' status of the animals afterwards.
        """
        for y in self.island_map:
            for cell in y:
                cell.migration()

        for y in self.island_map:
            for cell in y:
                for animal in cell.population:
                    animal.has_moved = False

    def island_aging(self):
        """
        Yearly cycle for aging. All animals on the island turn one year older.
        """
        for y in self.island_map:
            for cell in y:
                cell.aging()

    def island_loss_of_weight(self):
        """
        Yearly cycle for loss of weight. All animals on the island loses
        weight.
        """
        for y in self.island_map:
            for cell in y:
                cell.loss_of_weight()

    def island_deaths(self):
        """
        Yearly cycle for death. Checks for all animals on the island if the
        die.
        """
        for y in self.island_map:
            for cell in y:
                cell.deaths()

    def island_cycle(self):
        """
        Performs operations related to the annual cycle for one cell.
        """
        self.island_fodder_growth()
        self.island_feeding()
        self.island_procreate()
        self.island_migration()
        self.island_aging()
        self.island_loss_of_weight()
        self.island_deaths()
