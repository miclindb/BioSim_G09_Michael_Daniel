# -*- coding: utf-8 -*-

"""
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

import numpy as np


class Animals:
    """
    Superclass for Herbivores and Carnivores.

    """

    def __init__(self, age=0, weight=None):
        """
        Class constructor for Animals.
        Creates an animal with age, weight and fitness as attributes.

        Parameters
        ----------
        age: int
            Age of the animal. Default value is 0
        weight: float
            Weight of the animal. If no value is specified, the weight assigned
            is drawn from a gaussian distribution. Calculated in class method
            'calculate_weight'.
        """
        self.age = age
        if weight is None:
            self.weight = self.calculate_weight()
        else:
            self.weight = weight
        self.fitness = self.calculate_fitness()

    def calculate_weight(self):
        return np.random.normal(self.parameters['w_birth'],
                                self.parameters['sigma_birth'])

    def calculate_fitness(self):
        return (1 / (1 + np.exp(
            self.parameters['phi_age'] * (
                    self.age - self.parameters['a_half'])))) * (
                       1 / (1 + np.exp(self.parameters['phi_weight'] * (
                       self.weight - self.parameters['w_half']))))

    def update_fitness(self):
        self.fitness = self.calculate_fitness()

    def update_weight(self, eaten):
        """
        Weight update after feeding. Currently used for herbivore feeding and
        carnivore killing.

        Parameters
        ----------
        eaten: float
            Amount of relative fodder eaten.

        Returns
        -------
        float
            Weight adjustment.

        """
        return eaten * self.parameters['beta']

    # These are currently only used for tests.
    @property
    def get_fitness(self):
        return self.fitness

    @get_fitness.setter
    def get_fitness(self, value):
        self.fitness = value

    def death(self):
        """
        Determine whether an animal dies. The animal dies if the fitness of the
        animal is 0. The animal also has a fixed probability of dying each
        year.

        Returns
        -------
        Bool:
            'True' is the animal dies and 'False' otherwise.
        """

        if self.fitness == 0:
            return True
        elif np.random.uniform(0, 1) <= self.parameters['omega'] * (
                1 - self.fitness):
            return True
        else:
            return False

    def gives_birth(self, animal_object, n):
        """
        Animals have a chance to produce an offspring each year. This is
        decided by their weight and the amount of nearby same species animals.

        Gender plays no role in mating, and each animal can only give birth to
        one offspring each year at most.

        After a successful birth, the animal loses weight equal to a portion of
        the birth weight of the baby.

        Parameters
        ----------
        animal_object: class object
            The animal that has a chance to become pregnant.
        n: int
            Number of same species animals in the same cell.

        Returns
        -------
        bool:
        True if a newborn is successfully born.
        new_born_animal: class object
            Newborn animal.
        """

        if self.weight < self.parameters['zeta'] * \
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
            pass
        else:
            prob_birth = min(1,
                             self.parameters['gamma'] * self.fitness * (n - 1))
            if np.random.uniform(0, 1) <= prob_birth:
                if animal_object.__class__.__name__ == 'Herbivore':
                    new_born_animal = Herbivore()
                elif animal_object.__class__.__name__ == 'Carnivore':
                    new_born_animal = Carnivore()
                else:
                    pass
                self.weight -= self.parameters['xi'] * new_born_animal.weight
                return True, new_born_animal
            else:
                pass

    def migration(self, set_of_available_cells):
        """
        Animal attempts to migrate to one of the nearby cells.
        The movement is determined by the fitness of the animal and the fodder
        in the nearby cells.

        Parameters
        ----------
        set_of_available_cells: Set
            A set of four nearby available cells. The set can contain any cells
            with invalid landscape types. (i.e. landscape that cannot be
            traversed such as mountain or ocean).

        Returns
        -------
        move: something
            The cell the animal choose to migrate to. False if the animal
            does not migrate.
        """
        check_move = self.parameters['mu'] * self.fitness
        if check_move >= np.random.uniform(0, 1):
            fodder_abundance = []
            for cell in set_of_available_cells:
                e_k = cell.fodder / (
                            (nearby_same_species_animals + 1) * appetite)
                fodder_abundance.append(e_k)

        else:
            move = False

        return move


class Herbivore(Animals):
    """
    Subclass of Animals.
    """

    parameters = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'phi_age': 0.2,
        'phi_weight': 0.1,
        'mu': 0.25,
        'a_half': 40.0,
        'w_half': 10.0,
        'omega': 0.4,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'F': 10.0,
        'eta': 0.05,
        'DeltaPhiMax': None
    }

    def __init__(self, age=0, weight=None):
        super(Herbivore, self).__init__(age, weight)

    def feed(self, cell_fodder_info):
        """
        Herbivore feeding. Each year, the herbivore attempts to eat an amount
        of fodder. How much the herbivore actually eats depends on the
        available fodder in the cell.

        Parameters
        ----------
        cell_fodder_info: float
            Amount of available fodder in the cell.

        Returns
        -------
        eaten: float
            Amount of actually eaten fodder.

        """

        eaten = self.parameters['F']
        if cell_fodder_info < eaten:
            eaten = cell_fodder_info
            self.weight += self.update_weight(eaten)
            self.update_fitness()
            return eaten
        else:
            self.weight += self.update_weight(eaten)
            self.update_fitness()
            return eaten


class Carnivore(Animals):
    """
    Subclass of Animals.
    """
    parameters = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'phi_age': 0.4,
        'phi_weight': 0.4,
        'mu': 0.4,
        'a_half': 60.0,
        'w_half': 4.0,
        'omega': 0.9,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'F': 50.0,
        'eta': 0.125,
        'DeltaPhiMax': 10.0
    }

    def __init__(self, age=0, weight=None):
        super(Carnivore, self).__init__(age, weight)

    def kill(self, nearby_herbivores):
        """
        Carnivore attempts to kill a nearby herbivore. If the carnivore
        successfully kills the nearby herbivore, the carnivore's weight is
        updated and its fitness is re-evaluated.

        The carnivore continues to kill nearby herbivores until it is full or
        there are no more nearby herbivores.

        Parameters
        ----------
        nearby_herbivores: list
            List of herbivores residing in same cell as the carnivore.

        Returns
        -------
        killed_herbivore: list
            List containing all herbivore objects that was killed by the
            carnivore.
        """
        kill_attempt = 0
        eaten = 0
        killed_herbivores = []
        self.get_fitness = 11

        for herbivore in nearby_herbivores:
            while eaten < self.parameters['F'] and \
                    kill_attempt <= len(nearby_herbivores):
                print('runs')
                if self.fitness <= herbivore.fitness:
                    chance = 0
                elif 0 < self.fitness - herbivore.fitness <= \
                        self.parameters['DeltaPhiMax']:
                    chance = (self.fitness - herbivore.fitness) / \
                             self.parameters['DeltaPhiMax']
                else:
                    chance = 1

                if chance >= np.random.uniform(0, 1):
                    self.weight += self.update_weight(herbivore.weight)
                    self.update_fitness()
                    eaten += herbivore.weight
                    killed_herbivores.append(herbivore)
                    self.get_fitness = 11

                kill_attempt += 1

            return killed_herbivores
