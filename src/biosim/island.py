from src.biosim.cell import Ocean, Mountain, Jungle, Savannah, Desert
from src.biosim import cell
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

    def generate_nearby_cells(self):
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

                self.island_map[y][x].nearby_cells = list_of_nearby_cells

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

    def island_fodder_growth(self):
        for y in self.island_map:
            for cell in y:
                cell.fodder_growth()

    def island_feeding(self):
        for y in self.island_map:
            for cell in y:
                cell.feeding()

    def island_procreate(self):
        for y in self.island_map:
            for cell in y:
                cell.procreate()

    def island_migration(self):
        for y in self.island_map:
            for cell in y:
                cell.migration()

    def island_aging(self):
        for y in self.island_map:
            for cell in y:
                cell.aging()

    def island_loss_of_weight(self):
        for y in self.island_map:
            for cell in y:
                cell.loss_of_weight()

    def island_deaths(self):
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
