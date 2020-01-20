# -*- coding: utf-8 -*-

"""
Cell Module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

from biosim.animals import Herbivore, Carnivore
import pandas as pd
import numpy as np


class Cell:
    """
    Superclass for all cell types.
    """
    def __init__(self):
        """
        Constructor for cells.

        Parameters
        ----------
        coordinate: tuple
            For which two- dimensional coordinate value the cell is
            constructed. Default value is (0, 0).
        """
        self.coordinate = ()
        self.fodder = 0
        self.population = []
        self.nearby_cells = []

    @staticmethod
    def sort_population(population):
        sorted_population = sorted(population, key=lambda x: x.fitness,
                                 reverse=True)
        return sorted_population

    @staticmethod
    def calculate_relative_fodder(fodder, animal_species, number_of_same_species):
        return fodder / ((number_of_same_species + 1) * animal_species.parameters['F'])

    def nearby_relative_fodder(self, animal):
        relative_fodder_list = []

        if isinstance(animal, Herbivore):
            for nearby_cell in self.nearby_cells:
                fodder = nearby_cell.fodder
                number_of_same_species = len([animal for animal in nearby_cell.population if isinstance(animal, Herbivore)])
                relative_fodder = self.calculate_relative_fodder(fodder, Herbivore, number_of_same_species)
                relative_fodder_list.append((relative_fodder, nearby_cell))

        elif isinstance(animal, Carnivore):
            for nearby_cell in self.nearby_cells:
                number_of_same_species = len([animal for animal in nearby_cell.population if isinstance(animal, Carnivore)])
                nearby_herbivores = [animal for animal in nearby_cell.population if isinstance(animal, Herbivore)]
                fodder = sum([herbivore.weight for herbivore in nearby_herbivores])
                relative_fodder = self.calculate_relative_fodder(fodder, Carnivore, number_of_same_species)
                relative_fodder_list.append((relative_fodder, nearby_cell))

        return relative_fodder_list

    @property
    def herbivores_in_cell(self):
        herbivores = [animal for animal in self.population if isinstance(animal, Herbivore)]
        return len(herbivores)

    @property
    def carnivores_in_cell(self):
        carnivores = [animal for animal in self.population if isinstance(animal, Carnivore)]
        return len(carnivores)

    def feeding(self):
        sorted_herbivores = self.sort_population([animal for animal in self.population if isinstance(animal, Herbivore)])
        sorted_carnivores = self.sort_population([animal for animal in self.population if isinstance(animal, Carnivore)])
        self.population = sorted_herbivores + sorted_carnivores

        nearby_herbivores = sorted_herbivores
        killed_herbivores = []
        for animal in self.population:
            if isinstance(animal, Herbivore):
                fodder_eaten = animal.feed(self.fodder)
                self.fodder -= fodder_eaten
            else:
                killed_herbivores = animal.kill(nearby_herbivores)

            nearby_herbivores = [herbivore for herbivore in nearby_herbivores if herbivore not in killed_herbivores]
        self.population = nearby_herbivores + sorted_carnivores

    def procreate(self):
        """
        Annual birth.

        Parameters
        ----------
        n: int
            Number of nearby animals.
        animal_object: class object
            Object of the animal.

        Returns: Bool or class object
            False if birth is unsuccessful
            class object if a new baby is successfully born.
        -------

        """
        new_born_animals = []
        for animal in self.population:
            nearby_same_species = len([ani for ani in self.population if isinstance(ani, type(animal))])
            birth = animal.gives_birth(nearby_same_species)

            if birth is not None:
                new_born_animals.append(birth)

        for new_born_animal in new_born_animals:
            self.population.append(new_born_animal)

    def migration(self):
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

        self.population = [animal for animal in self.population if animal not in migrating_animals]
        for migration in migrations:
            migration[1].population.append(migration[0])

    def aging(self):
        for animal in self.population:
            animal.aging()

    def loss_of_weight(self):
        for animal in self.population:
            animal.loss_of_weight()

    def deaths(self):
        dead_animals = []
        for animal in self.population:
            if animal.death():
                dead_animals.append(animal)
        self.population = [animal for animal in self.population if animal not in dead_animals]

    def fodder_growth(self):
        if isinstance(self, Jungle):
            self.fodder = self.parameters['f_max']
        elif isinstance(self, Savannah):
            self.fodder = self.fodder + self.parameters['alpha'] * (self.parameters['f_max'] - self.fodder)


class Ocean(Cell):
    """
    Cell subclass for all ocean landscape types.
    Ocean landscape cannot be traversed and contains no food.
    """

    def __init__(self):
        super(Ocean, self).__init__()
        self.landscape_type = "O"


class Mountain(Cell):
    """
    Cell subclass for all mountain landscape types.
    Mountain landscape cannot be traversed and contains no food.
    """

    def __init__(self):
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
        super(Savannah, self).__init__()
        self.landscape_type = "S"
        self.fodder = self.parameters['f_max']


class Desert(Cell):
    """
    Cell subclass for all desert landscape types.
    Desert landscape can be traversed and contains no fodder.
    """

    def __init__(self):
        super(Desert, self).__init__()
        self.landscape_type = "D"
