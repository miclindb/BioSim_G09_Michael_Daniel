# -*- coding: utf-8 -*-
"""
A test for cell.py
"""
from src.biosim.cell import Cell, Ocean, Mountain, Jungle, Savannah, Desert
from src.biosim.animals import Carnivore, Herbivore


class TestCell:

    def test_sort_population(self):
        """
        Test that the sort_population static method sorts correctly based on
        the fitness of the animals. The first animal of the list shall have the
        highest fitness.
        """
        cell = Ocean()
        population = [Carnivore(age=10, weight=20),
                      Herbivore(age=5, weight=20),
                      Herbivore(age=10, weight=40),
                      Herbivore(age=3, weight=10)]

        sorted_from_fitness = cell.sort_population(population)

        assert sorted_from_fitness[0].fitness > sorted_from_fitness[1].fitness

    def test_calculate_relative_fodder(self):
        """
        Test that the calculate_relative_fodder static method calculates and
        returns the correct value for relative fodder.
        """
        cell = Jungle()
        relative_fodder = cell.calculate_relative_fodder(700, Herbivore, 100)

        assert relative_fodder == (70/101)

    def test_nearby_relative_fodder(self):
        """
        Test that the nearby_relative_fodder method returns a list of tuples
        with correct values for relative_fodder in nearby_cells.
        """
        cell = Jungle()
        cell.population = [Herbivore()]
        animal = cell.population[0]

        nearby_1 = Ocean()
        nearby_2 = Jungle()
        nearby_3 = Jungle()
        nearby_4 = Savannah()

        nearby_2.population = [Herbivore() for i in range(10)]
        nearby_4.population = [Herbivore() for i in range(20)]

        cell.nearby_cells = [nearby_1, nearby_2, nearby_3, nearby_4]

        relative_fodder_list = cell.nearby_relative_fodder(animal)

        assert relative_fodder_list == [(0.0, nearby_1),
                                        (float(80/11), nearby_2),
                                        (80.0, nearby_3),
                                        (float(10/7), nearby_4)]

    def test_herbivores_in_cell(self):
        """
        Test if herbivores_in_cell property returns the correct value for
        the number of herbivores in the cell.
        """
        cell = Savannah()
        cell.population = [Carnivore(), Carnivore(), Herbivore(), Herbivore(),
                           Herbivore(), Herbivore()]

        assert cell.herbivores_in_cell == 4

    def test_carnivores_in_cell(self):
        """
        Test if carnivores_in_cell property returns the correct value for
        the number of carnivores in the cell.
        """
        cell = Desert()
        cell.population = [Carnivore(), Carnivore(), Herbivore(), Herbivore(),
                           Herbivore(), Herbivore()]

        assert cell.carnivores_in_cell == 2

    def test_feeding_population_update(self):
        """
        Test if the feeding method updates the population correctly if at least
        one herbivore is eaten.
        """
        cell = Jungle()
        carnivore = Carnivore()
        carnivore.get_fitness = 11

        cell.population = [Herbivore(), Herbivore(), Herbivore(), carnivore]
        cell.feeding()

        assert cell.herbivores_in_cell < 3

    def test_feeding_fodder_update(self):
        """
        Test that the fodder in the cell is updated correctly after one
        feeding.
        """
        cell = Jungle()
        cell.fodder = 500

        cell.population = [Herbivore() for i in range(10)]
        Herbivore.parameters['F'] = 20

        cell.feeding()

        assert cell.fodder == 500 - 10 * 20


def test_fodder_cell():
    """
    Testing if a default landscape cell has fodder = 0 when initializing the
    Cell class.
    """
    test_cell = Cell()
    assert test_cell.fodder == 0


def test_ocean_landscape():
    """
    Testing if a the Ocean subclass returns the correct string describing
    landscape_type.
    """
    ocean_cell = Ocean()
    assert ocean_cell.landscape_type == 'O'


def test_ocean_fodder():
    """
    Testing if a the Ocean subclass returns the correct value for the amount
    of fodder in the cell.
    """
    ocean_cell = Ocean()
    assert ocean_cell.fodder == 0


def test_mountain_landscape():
    """
    Testing if a the Mountain subclass returns the correct string describing
    landscape_type.
    """
    mountain_cell = Mountain()
    assert mountain_cell.landscape_type == 'M'


def test_mountain_fodder():
    """
    Testing if a the Mountain subclass returns the correct value for the amount
    of fodder in the cell.
    """
    mountain_cell = Mountain()
    assert mountain_cell.fodder == 0


def test_jungle_landscape():
    """
    Testing if a the Jungle subclass returns the correct string describing
    landscape_type.
    """
    jungle_cell = Jungle()
    assert jungle_cell.landscape_type == 'J'


def test_jungle_fodder():
    """
    Testing if a the Jungle subclass returns the correct value for the amount
    of fodder in the cell right after initializing.
    """
    jungle_cell = Jungle()
    assert jungle_cell.fodder == jungle_cell.parameters['f_max']


def test_savannah_landscape():
    """
    Testing if a the Savannah subclass returns the correct string describing
    landscape_type.
    """
    savannah_cell = Savannah()
    assert savannah_cell.landscape_type == 'S'


def test_savannah_fodder():
    """
    Testing if a the Savannah subclass returns the correct value for the amount
    of fodder in the cell right after initializing.
    """
    savannah_cell = Savannah()
    assert savannah_cell.fodder == savannah_cell.parameters['f_max']


def test_desert_landscape():
    """
    Testing if a the Desert subclass returns the correct string describing
    landscape_type.
    """
    desert_cell = Desert()
    assert desert_cell.landscape_type == 'D'


def test_desert_fodder():
    """
    Testing if a the Desert subclass returns the correct value for the amount
    of fodder in the cell.
    """
    desert_cell = Desert()
    assert desert_cell.fodder == 0
