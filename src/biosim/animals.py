import numpy as np


class Animals:
    """

    """
    def __init__(self):
        self.age = 0
        self.weight = np.random.normal(self.parameters['w_birth'],
                                       self.parameters['sigma_birth'])#staticmethod?
        if self.weight <= 0:
            self.fitness = 0
        else:#Question for TA, staticmethod?
            self.fitness = (1 / (1 + np.exp(self.parameters['phi_age'] * (self.age - self.parameters['a_half'])))) * \
                           (1 / (1 + np.exp(
                               self.parameters['phi_weight'] * (self.weight - self.parameters['w_half']))))

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
        prob_birth = min(1, self.parameters['gamma'] * self.fitness * (N - 1))
        if np.random.uniform(0, 1) <= prob_birth:
            if self.weight < self.parameters['zeta'] *\
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
                self.weight -= self.parameters['xi'] *#birthweight
                return True
            else:
                return False


    def migration(self):


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
        f_eaten = 0
        fodder = #cell_info
        while not f_eaten != self.parameters['F']:
            #eat
            #Update cell info
        self.weight += self.parameters['beta'] * f_eaten

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
        'xi': 1.1
        'F': 50.0
        'DeltaPhiMax': 10.0
    }

    def __init__(self):
        super(Carnivore, self).__init__()

    def kill(self, nearby_herbivore):#Staticmethod/classmethod?
        if self.fitness <= nearby_herbivore.fitness:
            z = 0
        elif 0 < self.fitness - nearby_herbivore.fitness < self.parameters['DeltaPhiMax']:
            z = ((self.fitness - nearby_herbivore.fitness)/self.parameters['DeltaPhiMax'])
        else:
            z = 1



