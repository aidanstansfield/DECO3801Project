import unittest
import os.path
import sys

# PEP366 - don't even ask
if __package__ is None or __package__ == "":
	__package__ = "allocation"
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from . import constraints


all_students = ["0","1","2","3","4"]
older_students = ["2","3"]
younger_students = ["0","1","4"]
student_info = {
	"0": {"name":"Alice",   "age":18, "preferences":["ui", "networking", "graphics", "gameplay"]},
	"1": {"name":"Bob",     "age":19, "preferences":["ui", "networking"]},
	"2": {"name":"Charlie", "age":21, "preferences":["ui", "gameplay"]},
	"3": {"name":"Daniel",  "age":22, "preferences":[]},
	"4": {"name":"Eric",    "age":19, "preferences":["networking", "graphics"]}}



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
	

class TestSubsetSimilarityConstraint(unittest.TestCase):
	def setUp(self):
		self.similarity_constraint = constraints.SubsetSimilarityConstraint(
			"preference constraint", "preferences", 1,
			True, ("ui", "networking", "graphics", "gameplay"))
		self.diversity_constraint = constraints.SubsetSimilarityConstraint(
			"preference constraint", "preferences", 1,
			False, ("ui", "networking", "graphics", "gameplay"))
	
	def test_are_similar(self):
		cost = self.similarity_constraint.evaluate(older_students, student_info)
		self.assertEqual(cost, 0.5)
	
	def test_not_similar(self):
		cost = self.similarity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 2.75)
	
	def test_are_diverse(self):
		cost = self.diversity_constraint.evaluate(all_students, student_info)
		self.assertEqual(cost, 0.25)
	
	def test_not_doverse(self):
		cost = self.diversity_constraint.evaluate(younger_students, student_info)
		self.assertEqual(cost, 0.5)
	


if __name__=='__main__':
	unittest.main(verbosity=2)
