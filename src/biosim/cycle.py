from biosim.animals import Animals, Herbivore, Carnivore
from biosim.landscape import Cell, Jungle, Ocean, Mountain


class AnnualCycle:

    landscape_dict = {'J': Jungle(), 'O': Ocean(), 'M': Mountain()}

    def __init__(self):

        self.year = 0
        self.island_map = None

    def island_constructor(self, island_map):

        self.island_map = island_map
        cell = [landscape_dict[map]]
        animal_objects = [Herbivore() for i in range(10)]
        cell.append(animal_objects)
        self.island_map = pd.DataFrame([[cell]])


    def aging(self):

        for x in range(self.island_map.shape[0]):
            for y in range(self.island_map.shape[1]):
                for animal in self.island_map[x][y][1]:
                    animal.age += 1

    


def



from biosim.animals import Herbivore, Carnivore

map = """\
         J"""

self.island_map = textwrap.dedent(map)

landscape_dict = {'J': Jungle(), 'O': Ocean(), 'M': Mountain()}

cell = [landscape_dict[map]]

animal_objects = [Herbivore() for i in range(10)]

cell.append(animal_objects)

df = pd.DataFrame([[cell]])
