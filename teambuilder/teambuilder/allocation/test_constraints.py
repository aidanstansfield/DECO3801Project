# Unit tests to ensure constraints are evaluated correctly.

import unittest
import os.path
import sys

# PEP366 - don't even ask
if __package__ is None or __package__ == "":
	__package__ = "allocation"
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from . import constraints


# Data for testing
from .test_data import *


class TestIntegerCountConstraint(unittest.TestCase):
	def setUp(self):
		self.should_constraint = constraints.IntegerCountConstraint("age constraint",
			"age", 1, True, constraints.BXY(2,2), True, constraints.BXY(20,30))
		self.shouldnt_constraint = constraints.IntegerCountConstraint("age constraint",
			"age", 1, False, constraints.BXY(2,2), True, constraints.BXY(20,30))
	
	def test_should_met(self):
		cost = self.should_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_should_unmet(self):
		cost = self.should_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 2)
	
	def test_shouldnt_met(self):
		cost = self.shouldnt_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_shouldnt_unmet(self):
		cost = self.shouldnt_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 1)


class TestIntegerAverageConstraint(unittest.TestCase):
	def setUp(self):
		self.should_constraint = constraints.IntegerAverageConstraint(
			"age constraint", "age", 1, True, constraints.BXY(20,22))
		self.shouldnt_constraint = constraints.IntegerAverageConstraint(
			"age constraint", "age", 1, False, constraints.BXY(20,22))
	
	def test_should_met(self):
		cost = self.should_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_should_unmet(self):
		cost = self.should_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, (20-(56/3))/3)
	
	def test_shouldnt_met(self):
		cost = self.shouldnt_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_shouldnt_unmet(self):
		cost = self.shouldnt_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0.75)


class TestIntegerSimilarityConstraint(unittest.TestCase):
	def setUp(self):
		self.similarity_constraint = constraints.IntegerSimilarityConstraint(
			"age constraint", "age", 1, True)
		self.diversity_constraint = constraints.IntegerSimilarityConstraint(
			"age constraint", "age", 1, False)
	
	def test_are_similar(self):
		cost = self.similarity_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0.7071067811865476)
	
	def test_not_similar(self):
		cost = self.similarity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 1.6431676725154984)
	
	def test_are_diverse(self):
		cost = self.diversity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 1.1852594522306914)
	
	def test_not_diverse(self):
		cost = self.diversity_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 2.251076855556564)


class TestIntegerGlobalAverageConstraint(unittest.TestCase):
	def setUp(self):
		self.constraint = constraints.IntegerGlobalAverageConstraint(
			"global age constraint", "age", 1)
	
	def test_are_similar(self):
		cost = self.constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_not_similar(self):
		cost = self.constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 1.6999999999999993)


class TestOptionCountConstraint(unittest.TestCase):
	def setUp(self):
		self.should_constraint = constraints.OptionCountConstraint(
			"degree constraint", "degree", 1, True,
			constraints.BXY(2,2), True, "IT", degrees)
		self.shouldnt_constraint = constraints.OptionCountConstraint(
			"degree constraint", "degree", 1, False,
			constraints.BXY(2,2), True, "IT", degrees)
	
	def test_should_met(self):
		cost = self.should_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_should_unmet(self):
		cost = self.should_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 2)
	
	def test_shouldnt_met(self):
		cost = self.shouldnt_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_shouldnt_unmet(self):
		cost = self.shouldnt_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 1)


class TestOptionSimilarityConstraint(unittest.TestCase):
	def setUp(self):
		self.similarity_constraint = constraints.OptionSimilarityConstraint(
			"degree constraint", "degree", 1, True, degrees)
		self.diversity_constraint = constraints.OptionSimilarityConstraint(
			"degree constraint", "degree", 1, False, degrees)
	
	def test_are_similar(self):
		cost = self.similarity_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 1)
	
	def test_not_similar(self):
		cost = self.similarity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 3)
	
	def test_are_diverse(self):
		cost = self.diversity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0.6666666666666667)
	
	def test_not_diverse(self):
		cost = self.diversity_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 1)


class TestSubsetCountConstraint(unittest.TestCase):
	def setUp(self):
		self.should_constraint = constraints.SubsetCountConstraint(
			"preference constraint", "preferences", 1, True,
			constraints.BXY(2,3), True, "networking", degrees)
		self.shouldnt_constraint = constraints.SubsetCountConstraint(
			"preference constraint", "preferences", 1, False,
			constraints.BXY(2,3), True, "networking", degrees)
	
	def test_should_met(self):
		cost = self.should_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_should_unmet(self):
		cost = self.should_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 1)
	
	def test_shouldnt_met(self):
		cost = self.shouldnt_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_shouldnt_unmet(self):
		cost = self.shouldnt_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 1)


class TestSubsetSimilarityConstraint(unittest.TestCase):
	def setUp(self):
		self.similarity_constraint = constraints.SubsetSimilarityConstraint(
			"preference constraint", "preferences", 1, True, preferences)
		self.diversity_constraint = constraints.SubsetSimilarityConstraint(
			"preference constraint", "preferences", 1, False, preferences)
	
	def test_are_similar(self):
		cost = self.similarity_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0.5)
	
	def test_not_similar(self):
		cost = self.similarity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 2.75)
	
	def test_are_diverse(self):
		cost = self.diversity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0.25)
	
	def test_not_diverse(self):
		cost = self.diversity_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 0.5)


class TestBooleanCountConstraint(unittest.TestCase):
	def setUp(self):
		self.should_constraint = constraints.BooleanCountConstraint(
			"postgraduate constraint", "postgrad", 1, True,
			constraints.BXY(1,1), True)
		self.shouldnt_constraint = constraints.BooleanCountConstraint(
			"postgraduate constraint", "postgrad", 1, False,
			constraints.BXY(1,1), True)
	
	def test_should_met(self):
		cost = self.should_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_should_unmet(self):
		cost = self.should_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 1)
	
	def test_shouldnt_met(self):
		cost = self.shouldnt_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 0)
	
	def test_shouldnt_unmet(self):
		cost = self.shouldnt_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 1)


if __name__=='__main__':
	unittest.main(verbosity=2)
