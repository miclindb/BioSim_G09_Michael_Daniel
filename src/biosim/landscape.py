# -*- coding: utf-8 -*-

"""
Landscape module
"""

__author__ = "Michael Lindberg, Daniel Milliam Müller"
__email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"


class Cell:
    """
    Superclass for all cell types.
    """
    def __init__(self, coordinate=(0, 0)):
        """
        Constructor for cells.

        Parameters
        ----------
        coordinate: tuple
            For which two- dimensional coordinate value the cell is
            constructed. Default value is (0, 0).
        """
        self.coordinate = coordinate
        self.fodder = 0
        self.population = []


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
    Desert landscape can be traversed and contains no food.
    """

    def __init__(self):
        super(Desert, self).__init__()
        self.landscape_type = "D"
