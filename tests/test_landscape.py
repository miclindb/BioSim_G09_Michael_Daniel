"""
A test for cell.py
"""
from src.biosim.cell import Cell, Ocean, Mountain, Jungle, Savannah, Desert


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
