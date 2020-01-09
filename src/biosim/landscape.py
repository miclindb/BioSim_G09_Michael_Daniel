
class Cell:

    def __init__(self):

        self.location = (1, 1)

        self.fodder = 0
        self.population = []


class Ocean(Cell):

    def __init__(self):
        super(Ocean, self).__init__()

        self.landscape_type = "O"


class Mountain(Cell):

    def __init__(self):
        super(Mountain, self).__init__()

        self.landscape_type = "M"


class Jungle(Cell):

    parameters = {'f_max': 800.0}

    def __init__(self):
        super(Jungle, self).__init__()

        self.landscape_type = "J"

        self.fodder = self.parameters['f_max']


class Savannah(Cell):

    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        super(Savannah, self).__init__()

        self.landscape_type = "S"

        self.fodder = self.parameters['f_max']


class Desert(Cell):

    def __init__(self):
        super(Desert, self).__init__()

        self.landscape_type = "D"