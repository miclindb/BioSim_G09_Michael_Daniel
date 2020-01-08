import numpy as np


class Animals:
    """

    """
    def __init__(self):
        self.age = 0
        self.weight = np.random.normal(self.parameters['w_birth'],
                                       self.parameters['sigma_birth'])
        if self.weight <= 0:
            self.fitness = 0
        else:#Question for TA
            self.fitness = (1 / (1 + np.exp(self.parameters['phi_age'] * (self.age - self.parameters['a_half'])))) * \
                           (1 / (1 + np.exp(
                               self.parameters['phi_weight'] * (self.weight - self.parameters['w_half']))))
        self.pregnant = False

    def death(self):#Question for TA
        if self.fitness == 0:
            return True
        elif np.random.uniform(0, 1) <= self.parameters['omega'] * (1 - self.fitness):
            return True
        else:
            return False

    def gives_birth(self, N=4):
        prob_birth = min(1, self.parameters['gamma'] * self.fitness * (N - 1))
        if np.random.uniform(0, 1) <= prob_birth:

    def gives_birth(self):
        if self.weight < self.parameters['zeta'] *\
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):




    def migration(self):


class Herbivore(Animals):
    """

    """
    parameters = {
        'w_birth': 8.0,
        'sigma_birth': 1.5,
        'phi_age': 0.2,
        'phi_weight': 0.1,
        'a_half': 40.0,
        'w_half': 10.0,
        'omega': 0.4,
        'gamma': 0.2,
        'zeta': 3.5
    }

    def __init__(self):
        super(Herbivore, self).__init__()

    def feed(self):



