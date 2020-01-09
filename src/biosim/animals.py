import numpy as np
from biosim import landscape as ls# how to do this?


class Animals:
    def __init__(self, age=None):
        if age is None:
            self.age = 0
        self.weight = self.calculate_weight()
        self.fitness = self.calculate_fitness()


    @classmethod
    def calculate_weight(cls):
        return np.random.normal(cls.parameters['w_birth'],
                                       cls.parameters['sigma_birth'])

    @classmethod
    def calculate_fitness(cls):
        return ((1 / (1 + np.exp(cls.parameters['phi_age'] * (cls.age - cls.parameters['a_half'])))) * \
                       (1 / (1 + np.exp(
                           cls.parameters['phi_weight'] * (cls.weight - cls.parameters['w_half'])))))


    def death(self):#Question for TA, about random uniform
        """
        Class method for death. Used to determine whether an animal dies each year.
        Returns True if animals dies and False otherwise.

        :return:
        bool
        """
        if self.fitness == 0:
            return True
        elif np.random.uniform(0, 1) <= self.parameters['omega'] * (1 - self.fitness):
            return True
        else:
            return False

    def gives_birth(self, N=4):
        """
        Class method for birth.

        :param N: Number of other animals of same species in same cell
        :return:
        Bool
        """
        pass
        """
        prob_birth = min(1, self.parameters['gamma'] * self.fitness * (N - 1))
        if np.random.uniform(0, 1) <= prob_birth:
            if self.weight < self.parameters['zeta'] *\
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
                
                self.weight -= self.parameters['xi'] *#birthweight
                return True
            else:
                return False
        """

    def migration(self):
        pass


class Herbivore(Animals):
    """

    """
    parameters = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'phi_age': 0.2,
        'phi_weight': 0.1,
        'a_half': 40.0,
        'w_half': 10.0,
        'omega': 0.4,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'F': 10,
        'DeltaPhiMax': None
    }

    def __init__(self):
        super(Herbivore, self).__init__()

    def feed(self):
        """
        Class method for Herbivore feeding.
        :return: None
        """
        pass
        """
        location =
        if ls.cell.info.fodder < self.parameters['F']:
            eaten = differanse
        elif cell.info.fodder == 0
            eaten = 0
        else:
            eaten self.parameters['F']
        cell.update.fodder(-eaten)
        weight.update(eaten * beta)
        """


class Carnivore(Animals):
    """
    Test what parameters are used. Carnivore or Herbivore?
    """
    parameters = {
        'w_birth': 6.0,
        'sigma_birth': 1.0,
        'beta': 0.75,
        'phi_age': 0.4,
        'phi_weight': 0.4,
        'a_half': 60.0,
        'w_half': 4.0,
        'omega': 0.9,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'F': 50.0,
        'DeltaPhiMax': 10.0
    }

    def __init__(self):
        super(Carnivore, self).__init__()

    def kill(self, nearby_herbivore):
        pass

        """
        if self.fitness <= nearby_herbivore.fitness:
            z = 0
        elif 0 < self.fitness - nearby_herbivore.fitness < self.parameters['DeltaPhiMax']:
            z = ((self.fitness - nearby_herbivore.fitness)/self.parameters['DeltaPhiMax'])
        else:
            z = 1
            """
