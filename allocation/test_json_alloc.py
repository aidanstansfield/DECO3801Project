import json 
import unittest 
import json_alloc


# Data for testing
age_constraint = json_alloc.IntegerCountConstraint("age_constraint",
	"age", 1, True, json_alloc.BXY(2,2), True, json_alloc.BXY(20,30))

age_constraint_flat = {
	"constr_type": "IntegerCountConstraint",
	"name":        "age_constraint",
	"field":       "age",
	"priority":    1,
	"should_bool": True,
	"count_bxy":   [2, 2],
	"with_bool":   True,
	"value_bxy":   [20, 30]}

preference_constraint = json_alloc.SubsetSimilarityConstraint(
	"preference constraint", "preferences", 1,
	True, ("ui", "networking", "graphics", "gameplay"))

preference_constraint_flat = {
	"constr_type":  "SubsetSimilarityConstraint",
	"name":         "preference constraint",
	"field":        "preferences",
	"priority":     1,
	"similar_bool": True,
	"candidates":   ["ui", "networking", "graphics", "gameplay"]}

example_students = {
	"0": {"name":"Alice",   "age":18, "preferences":["ui", "networking", "graphics", "gameplay"]},
	"1": {"name":"Bob",     "age":19, "preferences":["ui", "networking"]},
	"2": {"name":"Charlie", "age":21, "preferences":["ui", "gameplay"]},
	"3": {"name":"Daniel",  "age":22, "preferences":[]},
	"4": {"name":"Eric",    "age":19, "preferences":["networking", "graphics"]}}



# Tests for the ConstraintEncoder class
class TestConstraintEncoder(unittest.TestCase):
	def test_BXY_point(self):
		bxy = json_alloc.BXY(3,3)
		output = json.dumps(bxy, cls=json_alloc.ConstraintEncoder)
		self.assertEqual(output, "[3, 3]")
	
	def test_BXY_range(self):
		bxy = json_alloc.BXY(2,4)
		output = json.dumps(bxy, cls=json_alloc.ConstraintEncoder)
		self.assertEqual(output, "[2, 4]")
	
	def test_encode_IntegerCountConstraint(self):
		output = json.dumps(age_constraint, cls=json_alloc.ConstraintEncoder)
		flat = json.loads(output)
		self.assertEqual(flat, age_constraint_flat)
		
	def test_encode_SubsetSimilarityConstraint(self):
		output = json.dumps(preference_constraint, cls=json_alloc.ConstraintEncoder)
		flat = json.loads(output)
		self.assertEqual(flat, preference_constraint_flat)


# Tests for the encode_request function
class TestEncodeRequest(unittest.TestCase):
	def setUp(self):
		self.encoded = json_alloc.encode_request(1, 2, 3, [age_constraint], example_students)
		self.flat = json.loads(self.encoded)
	
	def test_encode_min_size(self):
		self.assertEqual(self.flat["min_size"], 1)
	
	def test_encode_ideal_size(self):
		self.assertEqual(self.flat["ideal_size"], 2)
	
	def test_encode_max_size(self):
		self.assertEqual(self.flat["max_size"], 3)
	
	def test_encode_constraints(self):
		self.assertEqual(self.flat["constraints"], [age_constraint_flat])
	
	def test_encode_students(self):
		self.assertEqual(self.flat["students"], example_students)



if __name__=='__main__':
	unittest.main(verbosity=2) 
