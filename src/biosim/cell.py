# -*- coding: utf-8 -*-

"""
Cell Module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from biosim.animals import Herbivore, Carnivore


class Cell:
    """
    Superclass for all cell types.
    """

    def __init__(self):
        """
        Constructor for cells.
        """
        self.coordinate = ()
        self.fodder = 0
        self.population = []
        self.nearby_cells = []

    @staticmethod
    def sort_population(population):
        """
        Sorts a list of animals by their fitness in descending order.
        """
        sorted_population = sorted(
            population, key=lambda x: x.fitness, reverse=True
        )
        return sorted_population

    @staticmethod
    def calculate_relative_fodder(fodder, animal_species, same_species):
        """
        Calculates amount of relative fodder in a cell.

        Parameters
        ----------
        fodder: float
            fodder in cell
        animal_species: Animal
            Type of animal
        same_species: int
            Number of same species animals in cell

        Returns
        -------
        float:
            Amount of relative fodder in cell.
        """
        return fodder / (
                (same_species + 1) * animal_species.parameters['F']
        )

    def herbivore_nearby_fodder(self, relative_fodder_list):
        """
        Calculates the the amount of nearby fodder for herbivores.
        relative_fodder_list is a list containing the amount of fodder for each
        nearby cell.
        """
        for nearby_cell in self.nearby_cells:
            fodder = nearby_cell.fodder
            same_species = len(
                [animal for animal in nearby_cell.population if
                 isinstance(animal, Herbivore)])
            relative_fodder = self.calculate_relative_fodder(
                fodder, Herbivore, same_species
            )
            relative_fodder_list.append((relative_fodder, nearby_cell))

    def carnivore_nearby_fodder(self, relative_fodder_list):
        """
        Calculates the the amount of nearby fodder for carnivores.
        relative_fodder_list is a list containing the amount of fodder for each
        nearby cell.
        """
        for nearby_cell in self.nearby_cells:
            same_species = len(
                [animal for animal in nearby_cell.population if
                 isinstance(animal, Carnivore)])
            nearby_herbivores = [animal for animal in
                                 nearby_cell.population if
                                 isinstance(animal, Herbivore)]
            fodder = sum(
                [herbivore.weight for herbivore in nearby_herbivores])
            relative_fodder = self.calculate_relative_fodder(
                fodder, Carnivore, same_species
            )
            relative_fodder_list.append((relative_fodder, nearby_cell))

    def nearby_relative_fodder(self, animal):
        """
        Calculates the amount of fodder in nearby cells.

        Parameters
        ----------
        animal: Animal
            Either a class instance of Herbivore or Carnivore

        Returns
        -------
        relative_fodder_list: list
            List containing relative fodder in nearby cells and cell type of
            nearby cells.
        """
        relative_fodder_list = []

        if isinstance(animal, Herbivore):
            self.herbivore_nearby_fodder(relative_fodder_list)

        elif isinstance(animal, Carnivore):
            self.carnivore_nearby_fodder(relative_fodder_list)

        return relative_fodder_list

    @property
    def herbivores_in_cell(self):
        """
        Returns number of herbivores in cell.
        """
        herbivores = [animal for animal in self.population if
                      isinstance(animal, Herbivore)]
        return len(herbivores)

    @property
    def carnivores_in_cell(self):
        """
        Returns number of carnivores in cell.
        """
        carnivores = [animal for animal in self.population if
                      isinstance(animal, Carnivore)]
        return len(carnivores)

    def feeding(self):
        """
        Each animal in the cell attempts to feed.

        Each animal eats in order of their fitness. The most fit animal eats
        first.

        Feeding is different for herbivores and carnivores.
        Herbivores eat plant fodder and carnivores eat herbivores.

        Whenever a herbivore feeds, the amount of available fodder in the cell
        is reduced accordingly.
        Whenever a carnivore kills, the number of herbivores in the cell's
        population is reduced.
        """
        sorted_herbivores = self.sort_population(
            [animal for animal in self.population if
             isinstance(animal, Herbivore)]
        )
        sorted_carnivores = self.sort_population(
            [animal for animal in self.population if
             isinstance(animal, Carnivore)]
        )

        self.population = sorted_herbivores + sorted_carnivores

        nearby_herbivores = sorted_herbivores
        killed_herbivores = []
        for animal in self.population:
            if isinstance(animal, Herbivore):
                fodder_eaten = animal.feed(self.fodder)
                self.fodder -= fodder_eaten
            else:
                killed_herbivores = animal.kill(nearby_herbivores)

            nearby_herbivores = [herbivore for herbivore in nearby_herbivores
                                 if herbivore not in killed_herbivores]
        self.population = nearby_herbivores + sorted_carnivores

    def procreate(self):
        """
        Each animal in the cell attempts to procreate.

        Each animal can only mate with another animal that is of same
        species and currently in the same cell as itself.

        Each new born animal is added to the cell's population.
        """
        new_born_animals = []
        for animal in self.population:
            nearby_same_species = len(
                [ani for ani in self.population if isinstance(
                    ani, type(animal)
                )]
            )
            birth = animal.gives_birth(nearby_same_species)

            if birth is not None:
                new_born_animals.append(birth)

        for new_born_animal in new_born_animals:
            self.population.append(new_born_animal)

    def migration(self):
        """
        Each animal in the cell attempts to migrate if they haven't already
        migrated.

        Migration is decided by amount of relative fodder in nearby cells.
        For herbivores, relative fodder is plant fodder.
        For carnivores, relative fodder is herbivores.

        After an animal has migrated, its instance is removed from the cell's
        population list.
        """
        migrations = []
        if len(self.population) == 0:
            pass
        else:
            for animal in self.population:
                if animal.has_moved is False:
                    relative_fodder_list = self.nearby_relative_fodder(animal)
                    chosen_cell = animal.migrate(relative_fodder_list)
                    if chosen_cell is not None:
                        migrations.append((animal, chosen_cell))

        migrating_animals = []
        for migration in migrations:
            migrating_animals.append(migration[0])

        self.population = [animal for animal in self.population if
                           animal not in migrating_animals]
        for migration in migrations:
            migration[1].population.append(migration[0])

    def aging(self):
        """
        Updates animal age for all animals in cell.
        """
        for animal in self.population:
            animal.aging()

    def loss_of_weight(self):
        """
        Reduces animal weight for all animals in cell
        """
        for animal in self.population:
            animal.loss_of_weight()

    def deaths(self):
        """
        Checks whether an animal dies for all animals in cell. Dead animals are
        removed from the cell's population.
        """
        dead_animals = []
        for animal in self.population:
            if animal.death():
                dead_animals.append(animal)
        self.population = [animal for animal in self.population if
                           animal not in dead_animals]

    def fodder_growth(self):
        """
        Replenishes fodder for current cell.
        """
        if isinstance(self, Jungle):
            self.fodder = self.parameters['f_max']
        elif isinstance(self, Savannah):
            self.fodder = self.fodder + self.parameters['alpha'] * (
                    self.parameters['f_max'] - self.fodder
            )


class Ocean(Cell):
    """
    Cell subclass for all ocean landscape types.
    Ocean landscape cannot be traversed and contains no food.
    """

    def __init__(self):
        """
        Ocean initializer.
        """
        super(Ocean, self).__init__()
        self.landscape_type = "O"


class Mountain(Cell):
    """
    Cell subclass for all mountain landscape types.
    Mountain landscape cannot be traversed and contains no food.
    """

    def __init__(self):
        """
        Mountain initializer.
        """
        super(Mountain, self).__init__()
        self.landscape_type = "M"


class Jungle(Cell):
    """
    Cell subclass for all jungle landscape types.
    Jungle landscape can be traversed and available food is fully replenished
    every year.
    """

    parameters = {'f_max': 800.0}

    def __init__(self):
        """
        Jungle initializer.
        """
        super(Jungle, self).__init__()
        self.landscape_type = "J"
        self.fodder = self.parameters['f_max']


class Savannah(Cell):
    """
    Cell subclass for all savannah landscape types.
    Savannah landscape can be traversed and a portion of maximum available food
    is replenished every year.
    """

    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        """
        Savannah initializer.
        """
        super(Savannah, self).__init__()
        self.landscape_type = "S"
        self.fodder = self.parameters['f_max']


class Desert(Cell):
    """
    Cell subclass for all desert landscape types.
    Desert landscape can be traversed and contains no fodder.
    """

    def __init__(self):
        """
        Desert initializer.
        """
        super(Desert, self).__init__()
        self.landscape_type = "D"
