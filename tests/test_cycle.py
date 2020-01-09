"""
A test for cycle.py
"""
from src.biosim.cycle import AnnualCycle


def test_annual_cycle():
    """
    Testing that self.island_map is 'None' when initializing the
    AnnualCycle class.
    """
    test_cycle = AnnualCycle()
    assert test_cycle.island_map is None



