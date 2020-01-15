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
        self.tried_to_move = False

    def calculate_weight(self):
        return np.random.normal(self.parameters['w_birth'],
                                self.parameters['sigma_birth'])

    def aging(self):
        self.age += 1
        self.update_fitness()

    def loss_of_weight(self):
        self.weight -= self.weight * self.parameters['eta']
        self.update_fitness()

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

    def gives_birth(self, n):
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
                if self.__class__.__name__ == 'Herbivore':
                    new_born_animal = Herbivore()
                elif self.__class__.__name__ == 'Carnivore':
                    new_born_animal = Carnivore()
                else:
                    pass
                self.weight -= self.parameters['xi'] * new_born_animal.weight
                return new_born_animal
            else:
                pass

    def check_move(self):
        move = np.random.binomial(1, self.parameters['mu'] * self.fitness)
        return bool(move)

    def migrate(self, relative_fodder_list):
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
        self.tried_to_move = True

        if check_move is True:
            propensities = []
            for cell in relative_fodder_list:
                if cell[1].landscape_type == 'M' or 'O':
                    propensities.append(float(0))
                else:
                    propensities.append(np.exp(self.parameters['lambda']) * cell[0])
            probabilities = []
            for propensity in propensities:
                probabilities.append(propensity / sum(propensities))

            probabilities = np.array(probabilities)
            probabilities /= probabilities.sum()

            chosen_cell_index = list(np.random.choice(len(probabilities), 1, p=probabilities))
            chosen_cell = relative_fodder_list[chosen_cell_index[0]][1]

            return chosen_cell
        else:
            pass


class Herbivore(Animals):
    """
    Subclass of Animals.
    """

    parameters = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.0,
        'phi_age': 0.2,
        'w_half': 10.0,
        'phi_weight': 0.1,
        'mu': 0.25,
        'lambda': 1.0,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.0,
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
        'eta': 0.125,
        'a_half': 60.0,
        'phi_age': 0.4,
        'w_half': 4.0,
        'phi_weight': 0.4,
        'mu': 0.4,
        'lambda': 1.0,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.9,
        'F': 50.0,
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

        for herbivore in nearby_herbivores:
            if eaten < self.parameters['F'] and \
                    kill_attempt <= len(nearby_herbivores):
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
