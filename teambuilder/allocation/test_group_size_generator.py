import unittest
import os.path
import sys

# PEP366 - don't even ask
if __package__ is None or __package__ == "":
	__package__ = "allocation"
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from .group_size_generator import get_group_sizes
from .group_size_generator import ImpossibleConstraintsError

class TestGroupSizeMethod(unittest.TestCase):

    def test_negative_people(self):
        with self.assertRaises(ValueError):
            get_group_sizes(-2, 3, 4, 5)
    
    def test_not_enough_people(self):
        with self.assertRaises(ValueError):
            get_group_sizes(5, 6, 7, 8)
    
    def test_negative_min_size(self):
        with self.assertRaises(ValueError):
            get_group_sizes(10, -3, 4, 5)
    
    def test_negative_ideal_size(self):
        with self.assertRaises(ValueError):
            get_group_sizes(10, 3, -2, 5)
    
    def test_negative_max_size(self):
        with self.assertRaises(ValueError):
            get_group_sizes(10, 3, 4, -2)
    
    def test_ideal_smaller_than_min_size(self):
        with self.assertRaises(ValueError):
            get_group_sizes(10, 3, 2, 5)
    
    def test_max_smaller_than_min_size(self):
        with self.assertRaises(ValueError):
            get_group_sizes(10, 3, 4, 1)
    
    def test_max_smaller_than_ideal_size(self):
        with self.assertRaises(ValueError):
            get_group_sizes(10, 3, 5, 4)

    def test_valid_sizes_one_apart(self):
        groups = get_group_sizes(10, 3, 4, 5)
        expected = {5 : 2}      # Expect 2 groups of 5
        
        self.assertDictEqual(groups, expected, "Formed groups do not match")

    def test_valid_sizes_all_equal(self):
        groups = get_group_sizes(12, 4, 4, 4)
        expected = {4 : 3}

        self.assertDictEqual(groups, expected, "Formed groups do not match")

    def test_valid_sizes_several_apart(self):
        groups = get_group_sizes(24, 2, 5, 8)
        expected = {5 : 4, 4 : 1}

        self.assertDictEqual(groups, expected, "Formed groups do not match")

    def test_impossible_sizes_all_equal(self):
        with self.assertRaises(ImpossibleConstraintsError):
            groups = get_group_sizes(23, 3, 3, 3)

    def test_impossible_sizes_different_sizes(self):
        with self.assertRaises(ImpossibleConstraintsError):
            groups = get_group_sizes(11, 6, 6, 8)

if __name__=='__main__':
    unittest.main(verbosity=2)
