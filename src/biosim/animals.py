import numpy as np


# from biosim import landscape as ls# how to do this?
# Test change.


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
        self.fitness = self.calculate_fitness(self.age, self.weight)

    @classmethod
    def calculate_weight(cls):
        return np.random.normal(cls.parameters['w_birth'],
                                cls.parameters['sigma_birth'])

    @classmethod
    def calculate_fitness(cls, age, weight):
        return (1 / (1 + np.exp(
            cls.parameters['phi_age'] * (age - cls.parameters['a_half'])))) * (
                       1 / (1 + np.exp(cls.parameters['phi_weight'] * (weight - cls.parameters['w_half']))))

    @property
    def get_fitness(self):
        return self.fitness

    @get_fitness.setter
    def get_fitness(self, value):
        self.fitness = value

    def death(self):
        """
        Class method used to determine whether an animal dies.
        The animal dies if the fitness of the animal is 0. The animal also has
        a fixed probability of dying each year.

        Returns: Bool
            'True' is the animal dies and 'False' otherwise.
        -------

        """
        if self.fitness == 0:
            return True
        elif np.random.uniform(0, 1) <= self.parameters['omega'] * (
                1 - self.fitness):
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
    Subclass of Animals.
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
        'F': 10.0,
        'eta': 0.05,
        'DeltaPhiMax': None
    }

    def __init__(self, age=0, weight=None):
        super(Herbivore, self).__init__(age, weight)

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
    Subclass of Animals.
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
        'eta': 0.125,
        'DeltaPhiMax': 10.0
    }

    def __init__(self, age=0, weight=None):
        super(Carnivore, self).__init__(age, weight)

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
