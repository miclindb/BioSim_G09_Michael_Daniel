# -*- coding: utf-8 -*-

"""
Animals Module
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
        Creates an animal with age, weight, fitness and 'has_moved' as instance
        attributes.

        Parameters
        ----------
        age: int
            Age of the animal. Default value is 0.
        weight: float
            Weight of the animal. If no value is specified, the weight assigned
            is calculated in class method 'calculate_weight'.
        """
        self.age = age
        if weight is None:
            self.weight = self.calculate_weight()
        else:
            self.weight = weight
        self.fitness = self.calculate_fitness()
        self.has_moved = False

    def aging(self):
        """
        Increases the age of the animal by one year and updates its fitness.
        """
        self.age += 1
        self.update_fitness()

    def calculate_weight(self):
        """
        Calculates the weight of the animal. This is used whenever the class
        initializer for the animals did not receive any specified weight input.

        Returns
        -------
        float
            Weight of the animal.
        """
        return np.random.normal(self.parameters['w_birth'],
                                self.parameters['sigma_birth'])

    def loss_of_weight(self):
        """
        Calculates the amount of weight an animal loses every year, and updates
        the animals weight and fitness.
        """
        self.weight -= self.weight * self.parameters['eta']
        self.update_fitness()

    def weight_gain(self, eaten):
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

    def calculate_fitness(self):
        """
        Calculates the fitness of an animal.

        Returns
        -------
        float
            Fitness of the animal
        """
        if self.weight <= 0:
            return 0
        else:  # MATH?
            return (1 / (1 + np.exp(
                self.parameters['phi_age'] * (
                        self.age - self.parameters['a_half'])))) * \
                   (1 / (1 + np.exp(-(self.parameters['phi_weight'] *
                                      (self.weight - self.parameters[
                                          'w_half'])))))

    def update_fitness(self):
        """
        Updates the fitness of an animal.
        """
        self.fitness = self.calculate_fitness()

    @property
    def get_fitness(self):
        """
        Fitness getter for animals.

        Returns
        -------
        float
            Animal fitness
        """
        return self.fitness

    @get_fitness.setter
    def get_fitness(self, value):
        """
        Fitness setter for animals.

        Parameters
        ----------
        value: float
            Fitness value
        """
        self.fitness = value

    def death(self):
        """
        Determines whether an animal dies. The animal dies if the fitness of
        the animal is 0. The animal also has a probability of dying each year.

        Returns
        -------
        Bool
            'True' is the animal dies and 'False' otherwise.
        """

        if self.fitness == 0:
            return True
        elif bool(np.random.binomial(1, self.parameters['omega'] * (
                1 - self.fitness))) is True:
            return True
        else:
            return False

    @classmethod
    def weight_check_for_pregnancy(cls):
        """
        Checks whether the animal's weight is above a threshold. This is
        required for the animal to potentially get pregnant.

        Returns
        -------
        float
            Threshold value for pregnancy.
        """
        return cls.parameters['zeta'] * (
                cls.parameters['w_birth'] + cls.parameters['sigma_birth']
        )

    def probability_birth(self, n):
        """
        Calculates the probability of birth.

        Parameters
        ----------
        n: int
            Nearby same species animals

        Returns
        -------
        float
            Probability of birth
        """
        return min(1, self.parameters['gamma'] * self.fitness * (n - 1))

    def adjust_weight_after_birth(self, new_born_animal):
        """
        Updates the weight of the mother after a baby is born.

        Parameters
        ----------
        new_born_animal: Class object
            New born baby
        """
        self.weight -= self.parameters['xi'] * new_born_animal.weight

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
        n: int
            Number of same species animals in the same cell.

        Returns
        -------
        bool
            True if a newborn is successfully born.
        new_born_animal: class object
            Newborn animal.
        """

        if self.weight >= self.weight_check_for_pregnancy():
            if bool(np.random.binomial(1, self.probability_birth(n))) is True:
                if isinstance(self, Herbivore):
                    new_born_animal = Herbivore()
                else:
                    new_born_animal = Carnivore()
                self.adjust_weight_after_birth(new_born_animal)
                return new_born_animal
            else:
                pass
        else:
            pass

    def check_move(self):
        """
        Checks if an animal can move. This is checked every time an animal
        attempts to migrate.

        Returns
        -------
        bool
            'True' if the check is passed, 'False' otherwise.
        """
        return bool(
            np.random.binomial(1, self.parameters['mu'] * self.fitness)
        )

    @staticmethod
    def choose_migration_destination(relative_fodder_list, propensities_list):
        """
        Calculates which cell the animal decides to migrate to.

        Parameters
        ----------
        relative_fodder_list: list
            A list of up to four nearby available cells. The list can contain
            any cells with invalid landscape types. (i.e. landscape that cannot
            be traversed such as mountain or ocean).
        propensities_list: list
            List containing propensity values for each relevant cell.

        Returns
        -------
        chosen_cell: Cell object
            The cell the animal choose to migrate to.
        """
        probabilities = []
        for propensity in propensities_list:
            probabilities.append(propensity / sum(propensities_list))

        probabilities = np.array(probabilities)
        probabilities /= probabilities.sum()

        chosen_cell_index = \
            list(np.random.choice(len(probabilities), 1, p=probabilities))[
                0]

        chosen_cell = relative_fodder_list[chosen_cell_index][1]
        return chosen_cell

    def migrate(self, relative_fodder_list):
        """
        Animal attempts to migrate to one of the nearby cells.
        The movement is determined by the fitness of the animal and the fodder
        in the nearby cells.

        The animal migrates only once per year, and the animal's 'has_moved'
        status is updated to 'True' after.

        Parameters
        ----------
        relative_fodder_list: List
            A list of up to four nearby available cells. The list can contain
            any cells with invalid landscape types. (i.e. landscape that cannot
            be traversed such as mountain or ocean).

        Returns
        -------
        chosen_cell: Cell object
            The cell the animal choose to migrate to. Otherwise returns None if
            the animal does not move.
        """

        if self.check_move() is True:
            propensities = []
            for cell in relative_fodder_list:
                if cell[1].landscape_type == 'M':
                    propensities.append(float(0))
                elif cell[1].landscape_type == 'O':
                    propensities.append(float(0))
                else:
                    propensities.append(
                        np.exp(self.parameters['lambda']) * cell[0])
            #probabilities = []

            if sum(propensities) == 0:
                return None

            else:
                chosen_cell = self.choose_migration_destination(
                    relative_fodder_list, propensities
                )

            #for propensity in propensities:
            #    probabilities.append(propensity / sum(propensities))

            #probabilities = np.array(probabilities)
            #probabilities /= probabilities.sum()

            #chosen_cell_index = \
            #    list(np.random.choice(len(probabilities), 1, p=probabilities))[
                    #0]
            #chosen_cell = relative_fodder_list[chosen_cell_index][1]

            self.has_moved = True
            return chosen_cell

        else:
            return None


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
            self.weight += self.weight_gain(eaten)
            self.update_fitness()
            return eaten
        else:
            self.weight += self.weight_gain(eaten)
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

    def fitness_greater_than_prey(self, prey):
        """
        Checks if carnivore's fitness is greater than the herbivore's fitness,
        and not greater than a threshold.

        Parameters
        ----------
        prey: Class object
            The animal the carnivore is trying to kill.

        Returns
        -------
        bool
            'True' if the carnivore's fitness is greater than the herbivore's,
            and not greater than 'DeltaPhiMax' threshold. 'False' otherwise.

        """
        return 0 < self.fitness - prey.fitness <= self.parameters[
            'DeltaPhiMax']

    def chance_of_kill(self, prey):
        """
        The chance the carnivore has to kill its prey.

        Parameters
        ----------
        prey: Class object
            The animal the carnivore is trying to kill.

        Returns
        -------
        float
            Probability of killing prey.
        """
        return (self.fitness - prey.fitness) / self.parameters['DeltaPhiMax']

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
        kill_attempts = 0
        eaten = 0
        killed_herbivores = []
        number_of_nearby_herbivores = len(nearby_herbivores)

        for herbivore in nearby_herbivores:
            if eaten < self.parameters['F'] and \
                    kill_attempts <= number_of_nearby_herbivores:
                if self.fitness <= herbivore.fitness:
                    chance = 0
                elif self.fitness_greater_than_prey(herbivore):
                    chance = self.chance_of_kill(herbivore)
                else:
                    chance = 1

                if bool(np.random.binomial(1, chance)) is True:
                    self.weight += self.weight_gain(herbivore.weight)
                    self.update_fitness()
                    eaten += herbivore.weight
                    killed_herbivores.append(herbivore)

                kill_attempts += 1

        return killed_herbivores
