Examples
========

BioSim simulation for something, ex 1
-------------------------------------
Some example description.

.. code-block:: python

    from biosim.simulation import BioSim
    import matplotlib.pyplot as plt
    import textwrap

    if __name__ == '__main__':
        plt.ion()

        base = '..'

        geogr = """\
                   OOOOOOOOOOOOOOOOOOOOO
                   OOOOOOOOSMMMMJJJJJJJO
                   OSSSSSJJJJMMJJJJJJJOO
                   OSSSSSSSSSMMJJJJJJOOO
                   OSSSSSJJJJJJJJJJJJOOO
                   OSSSSSJJJDDJJJSJJJOOO
                   OSSJJJJJDDDJJJSSSSOOO
                   OOSSSSJJJDDJJJSOOOOOO
                   OSSSJJJJJDDJJJJJJJOOO
                   OSSSSJJJJDDJJJJOOOOOO
                   OOSSSSJJJJJJJJOOOOOOO
                   OOOSSSSJJJJJJJOOOOOOO
                   OOOOOOOOOOOOOOOOOOOOO"""
        geogr = textwrap.dedent(geogr)

        ini_herbs = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Herbivore", "age": 5, "weight": 20}
                    for _ in range(150)
                ],
            }
        ]
        ini_carns = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(40)
                ],
            }
        ]

        sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456, img_base=base)

        sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
        sim.set_animal_parameters(
            "Carnivore",
            {
                "a_half": 70,
                "phi_age": 0.5,
                "omega": 0.3,
                "F": 65,
                "DeltaPhiMax": 9.0,
            },
        )
        sim.set_landscape_parameters("J", {"f_max": 700})

        sim.simulate(num_years=10, vis_years=1, img_years=5)

        sim.add_population(population=ini_carns)

        sim.simulate(num_years=10, vis_years=1, img_years=5)

        plt.savefig("check_sim.pdf")


BioSim simulation for something, ex 2
-------------------------------------
Some example description.

.. code-block:: python

    """
    :mod:`biosim.population_generator` generates several populations of animals
    with age and weight randomly distributed and returns a list of dictionaries
    with the animals and the coordinates they are to be put.

    The user can define:
    #. The number of each species that are put on every defined coordinate
    #. The coordinates that the animals in that species should occupy

    If different sizes of the population within an species is preferable,
    the user can simply make another population and add it to the island

    Example of list returned:
    -------------------------
    ::

        [{'loc': (3,4),
          'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 15},
                  {'species': 'Herbivore', 'age': 5, 'weight': 40},
                  {'species': 'Herbivore', 'age': 15, 'weight': 25}]},
         {'loc': (4,4),
          'pop': [{'species': 'Herbivore', 'age': 2, 'weight': 60},
                  {'species': 'Herbivore', 'age': 9, 'weight': 30},
                  {'species': 'Herbivore', 'age': 16, 'weight': 14}]},
         {'loc': (4,4),
          'pop': [{'species': 'Carnivore', 'age': 3, 'weight': 35},
                  {'species': 'Carnivore', 'age': 5, 'weight': 20},
                  {'species': 'Carnivore', 'age': 8, 'weight': 5}]}]

    """
    __author__ = "Ragnhild Smistad, UMB and Toril Fjeldaas Rygg, UMB"

    import random


    class Population(object):
        """
        The population on the island
        """

        def __init__(
            self,
            n_herbivores=None,
            coord_herb=None,
            n_carnivores=None,
            coord_carn=None,
        ):
            """
            ==============    ==============================================
            *n_herbivores*    The number of herbivores in each coordinate
            *coord_herb*      A list of the different coordinates(tuple)
            *n_carnivores*    The number of carnivores in each coordinate
            *coord_carn*      A list of the different coordinates as tuple
            ==============    ==============================================
            """
            self.animals = []
            self.n_herb = n_herbivores
            self.n_carn = n_carnivores
            self.coord_herb = coord_herb
            self.coord_carn = coord_carn

        def get_animals(self):
            """
            Returns a complete list of dictionaries with a population for
            every coordinate defined.
            """
            if self.n_herb:
                for coord in self.coord_herb:
                    self.animals.append({"loc": coord, "pop": []})

                    for _ in range(self.n_herb):
                        self.animals[-1]["pop"].append(
                            {
                                "species": "Herbivore",
                                "age": random.randint(0, 20),
                                "weight": random.randint(5, 80),
                            }
                        )

            if self.n_carn:
                for coord in self.coord_carn:
                    self.animals.append({"loc": coord, "pop": []})
                    for _ in range(self.n_carn):
                        self.animals[-1]["pop"].append(
                            {
                                "species": "Carnivore",
                                "age": random.randint(0, 10),
                                "weight": random.randint(3, 50),
                            }
                        )
            return self.animals
