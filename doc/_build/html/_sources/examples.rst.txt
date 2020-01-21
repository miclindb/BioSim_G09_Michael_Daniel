Examples
========

BioSim simulation
-------------------------------------
Runs a standard simulation for 20 years.

.. code-block:: python

    import textwrap
    from biosim.simulation import BioSim

    """
    Runs a simulation for 20 years. The initial population on the island is 150
    herbivores and 200 carnivores.
    """

    __author__ = "Michael Lindberg, Daniel Milliam Müller"
    __email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

    if __name__ == "__main__":

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
                   OOOOOOOOOOOOOOOOOOOOO"""

        geogr = textwrap.dedent(geogr)

        ini_herbs = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Herbivore", "age": 10, "weight": 60}
                    for _ in range(150)
                ],
            }
        ]
        ini_carns = [
            {
                "loc": (10, 10),
                "pop": [
                    {"species": "Carnivore", "age": 6, "weight": 10}
                    for _ in range(200)
                ],
            }
        ]

        sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)
        sim.add_population(population=ini_carns)

        sim.simulate(num_years=20, vis_years=1, img_years=2000)


| **Simulation results**
| Map of Rossumøya after 20 years.

.. image:: simulation_results_20_years.jpg
   :width: 1500px
   :height: 1000px
   :scale: 50 %
   :alt: alternate text
   :align: center

BioSim simulation with movie creation
-------------------------------------
This simulation creates a MPEG4 movie that shows how the island updates over
the course of the simulation. The simulation runs for a total of 300 years.

.. code-block:: python

    import textwrap
    import matplotlib.pyplot as plt
    from biosim.simulation import BioSim

    """
    Runs a simulation for a total of 300 years. The initial population on the
    island is 150 herbivores and 40 carnivores.

    The parameters for the herbivores and carnivores are tweaked, which affects
    behaviour such as feeding, migration and birth.
    """

     __author__ = "Michael Lindberg, Daniel Milliam Müller"
    __email__ = "michael.lindberg@nmbu.no, daniel.milliam.muller@nmbu.no"

    import textwrap
    import matplotlib.pyplot as plt

    from biosim.simulation import BioSim

    if __name__ == "__main__":
        plt.ion()

        base = '../biosim_graphics/'

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

        sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)

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

        sim.simulate(num_years=100, vis_years=1, img_years=1)

        sim.add_population(population=ini_carns)

        sim.simulate(num_years=200, vis_years=1, img_years=1)

        sim.make_movie()

| **Simulation results**
| Map of Rossumøya after 300 years.

.. image:: simulation_results_300_years.jpg
   :width: 1500px
   :height: 1000px
   :scale: 50 %
   :alt: alternate text
   :align: center
