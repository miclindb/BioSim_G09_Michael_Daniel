from src.biosim.landscape import Ocean, Mountain, Jungle, Savannah, Desert
from src.biosim import landscape
from src.biosim.animals import Herbivore, Carnivore


class Island:

    def __init__(self, island_map):

        self.island_map = island_map

        self.landscape_dict = {'M': Mountain, 'O': Ocean, 'J': Jungle,
                          'S': Savannah, 'D': Desert}

        self.map_population = []

    def map_constructor(self):

        self.island_map = self.island_map.split('\n')

        for n in range(len(self.island_map)):
            self.island_map[n] = \
                [character for character in self.island_map[n]]

        for y in range(len(self.island_map)):
            for x in range(len(self.island_map[y])):
                self.island_map[y][x] = self.landscape_dict[self.island_map[y][x]]()
                self.island_map[y][x].coordinate = (y, x)

    def nearby_cells(self):
        for y in range(len(self.island_map)):
            for x in range(len(self.island_map[y])):
                list_of_nearby_cells = []
                if y != 0:
                    cell_1 = self.island_map[y-1][x]
                    list_of_nearby_cells.append(cell_1)
                if x != 0:
                    cell_2 = self.island_map[y][x-1]
                    list_of_nearby_cells.append(cell_2)
                if y != len(self.island_map)-1:
                    cell_3 = self.island_map[y+1][x]
                    list_of_nearby_cells.append(cell_3)
                if x != len(self.island_map[y])-1:
                    cell_4 = self.island_map[y][x+1]
                    list_of_nearby_cells.append(cell_4)

                self.island_map[y][x].nearby_cells = set(list_of_nearby_cells)

    def adding_population(self, population):
        for animals in population:
            self.map_population.append(animals)

        for animals in self.map_population:
            for animal in animals['pop']:
                if animal['species'] == 'Herbivore':
                    self.island_map[animals['loc'][0]][animals['loc'][1]].population.append(
                        Herbivore(age=animal['age'], weight=animal['weight']))
                if animal['species'] == 'Carnivore':
                    self.island_map[animals['loc'][0]][animals['loc'][1]].population.append(
                        Carnivore(age=animal['age'], weight=animal['weight']))

    def annual_cycle(self):
        """
        Performs operations related to the annual cycle for one cell.
        """
        for y in self.island_map:
            for cell in y:
                cell.feeding()  # Each animal feeds
                cell.procreate()  # Checks for birth for all animals
                cell.migrate()  # Each animal moves
                cell.aging()  # Updates age for all animals
                cell.loss_of_weight()  # Each animal loses weight
                cell.deaths()  # For each animal, we check if the animal dies