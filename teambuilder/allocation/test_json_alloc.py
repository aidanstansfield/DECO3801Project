import json 
import unittest
import os.path
import sys

# PEP366 - don't even ask
if __package__ is None or __package__ == "":
	__package__ = "allocation"
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from . import json_alloc


# Data for testing
age_constraint = json_alloc.IntegerCountConstraint("age constraint",
	"age", 1, True, json_alloc.BXY(2,2), True, json_alloc.BXY(20,30))

age_constraint_flat = {
	"constr_type": "IntegerCountConstraint",
	"name":        "age constraint",
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

example_students_json = json.dumps(example_students)

example_teams = {
	"0": ["0", "2"],
	"1": ["3", "1", "4"]}

example_request_flat = {
	"min_size":    1,
	"ideal_size":  2,
	"max_size":    3,
	"constraints": [age_constraint_flat],
	"students":    example_students}



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


# Tests for the encode_teams function
class TestEncodeTeams(unittest.TestCase):
	def setUp(self):
		self.encoded = json_alloc.encode_teams(example_teams)
		self.flat = json.loads(self.encoded)
	
	def test_keys(self):
		keys = self.flat.keys()
		self.assertEqual(len(keys), 2)
		self.assertTrue("success" in keys)
		self.assertTrue("teams" in keys)
	
	def test_success(self):
		self.assertTrue(self.flat["success"])
	
	def test_teams(self):
		self.assertEqual(self.flat["teams"], example_teams)


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


# Tests for the decode_request function
class TestDecodeRequest(unittest.TestCase):
	def setUp(self):
		self.valid_encoded = json.dumps(example_request_flat)
		self.valid_decoded = json_alloc.decode_request(self.valid_encoded)
	
	def test_decode_valid_min_size(self):
		self.assertEqual(self.valid_decoded[0], 1)
	
	def test_decode_valid_ideal_size(self):
		self.assertEqual(self.valid_decoded[1], 2)
	
	def test_decode_valid_max_size(self):
		self.assertEqual(self.valid_decoded[2], 3)
	
	def test_decode_valid_students(self):
		self.assertEqual(self.valid_decoded[3], example_students)
	
	def test_decode_valid_constraint_count(self):
		self.assertEqual(len(self.valid_decoded[4]), 1)
	
	def test_decode_valid_constraint(self): # very weak
		self.assertEqual(type(self.valid_decoded[4][0]), type(age_constraint))
	
	def test_decode_no_min_size(self):
		request = """{
			"ideal_size":  2,
			"max_size":    3,
			"constraints": [],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid minimum size")
	
	def test_decode_no_ideal_size(self):
		request = """{
			"min_size":    1,
			"max_size":    3,
			"constraints": [],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid ideal size")
	
	def test_decode_no_max_size(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"constraints": [],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid maximum size")
	
	def test_decode_no_students(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"constraints": []}"""
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid student info")
	
	def test_decode_no_constraints(self): # This is fine, gives empty constraint list
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"students":    """+example_students_json+"}"
		decoded = json_alloc.decode_request(request)
		self.assertEqual(decoded[4], [])
	
	def test_decode_invalid_request(self):
		request = '"Hello World!"'
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid request")
	
	def test_decode_invalid_request_json(self):
		request = "{[{o/!{/{{%{"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid JSON")
	
	def test_decode_invalid_min_size(self):
		request = """{
			"min_size":    "foo",
			"ideal_size":  2,
			"max_size":    3,
			"constraints": [],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid minimum size")
	
	def test_decode_invalid_ideal_size(self):
		request = """{
			"min_size":    1,
			"ideal_size":  "bar",
			"max_size":    3,
			"constraints": [],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid ideal size")
	
	def test_decode_invalid_max_size(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    "baz",
			"constraints": [],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid maximum size")
	
	def test_decode_invalid_students(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"constraints": [],
			"students":    "foobar"}"""
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid student info")
	
	def test_decode_invalid_constraint_list(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"constraints": "barbazz",
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid constraint list")
	
	def test_decode_invalid_constraint_type(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"constraints": [{
				"constr_type": "NotARealConstraint",
				"candidates": ["ui","networking","graphics","gameplay"],
				"field": "preferences",
				"name": "preference constraint",
				"priority": 1,
				"similar_bool": true}],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			print(json_alloc.decode_request(request))
		self.assertEqual(cm.exception.message, "Invalid constraint JSON")
	
	def test_decode_invalid_constraint_attr(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"constraints": [{
				"constr_type": "SubsetSimilarityConstraint",
				"candidates": ["ui","networking","graphics","gameplay"],
				"qwaszx": "preferences",
				"name": "preference constraint",
				"priority": 1,
				"similar_bool": true}],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid JSON for constraint (preference constraint)")
	
	def test_decode_invalid_constraint_bxy(self):
		request = """{
			"min_size":    1,
			"ideal_size":  2,
			"max_size":    3,
			"constraints": [{
				"constr_type": "IntegerCountConstraint",
				"count_bxy": [2,5,2],
				"field": "age",
				"name": "age_constraint",
				"priority": 1,
				"should_bool": true,
				"value_bxy": [20,30],
				"with_bool": true}],
			"students":    """+example_students_json+"}"
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.decode_request(request)
		self.assertEqual(cm.exception.message, "Invalid JSON for constraint (age_constraint)")


# Tests for the validate_request function
class TestValidateRequest(unittest.TestCase):
	def test_valid(self):
		json_alloc.validate_request("foobar", 1, 2, 3, example_students, [age_constraint])
	
	def test_misorder_min_ideal(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_request("foobar", 2, 1, 3, example_students, [age_constraint])
		self.assertEqual(cm.exception.message, "Invalid group size ordering")
	
	def test_misorder_ideal_max(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_request("foobar", 1, 3, 2, example_students, [age_constraint])
		self.assertEqual(cm.exception.message, "Invalid group size ordering")
	
	def test_misorder_min_max(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_request("foobar", 3, 2, 1, example_students, [age_constraint])
		self.assertEqual(cm.exception.message, "Invalid group size ordering")
	
	def test_invalid_student(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_request("foobar", 1, 2, 3, {"asdf":42}, [age_constraint])
		self.assertEqual(cm.exception.message, "Invalid student data")


# Tests for the validate_constraint function
class TestValidateConstraint(unittest.TestCase):
	def setUp(self):
		self.no_fields = {
			"0": {"name":"Alice"},
			"1": {"name":"Bob"},
			"2": {"name":"Charlie"},
			"3": {"name":"Daniel"},
			"4": {"name":"Eric"}}
		self.wrong_type = {
			"0": {"name":"Alice",   "preferences":18, "age":["ui", "networking", "graphics", "gameplay"]},
			"1": {"name":"Bob",     "preferences":19, "age":["ui", "networking"]},
			"2": {"name":"Charlie", "preferences":21, "age":["ui", "gameplay"]},
			"3": {"name":"Daniel",  "preferences":22, "age":[]},
			"4": {"name":"Eric",    "preferences":19, "age":["networking", "graphics"]}}
	
	def test_integer_constraint_valid(self):
		json_alloc.validate_constraint("foobar", example_students, age_constraint)
	
	def test_integer_constraint_no_field(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_constraint("foobar", self.no_fields, age_constraint)
		self.assertEqual(cm.exception.message, "Constraint (age constraint) is on a missing student info field (age)")
	
	def test_integer_constraint_wrong_type(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_constraint("foobar", self.wrong_type, age_constraint)
		self.assertEqual(cm.exception.message, "Constraint (age constraint) type (integer) doesn't match student info field (age) type")
	
	def test_subset_constraint_valid(self):
		json_alloc.validate_constraint("foobar", example_students, preference_constraint)
	
	def test_subset_constraint_no_field(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_constraint("foobar", self.no_fields, preference_constraint)
		self.assertEqual(cm.exception.message, "Constraint (preference constraint) is on a missing student info field (preferences)")
	
	def test_subset_constraint_wrong_type(self):
		with self.assertRaises(json_alloc.InvalidRequestError) as cm:
			json_alloc.validate_constraint("foobar", self.wrong_type, preference_constraint)
		self.assertEqual(cm.exception.message, "Constraint (preference constraint) type (subset) doesn't match student info field (preferences) type")


# Tests for the allocate function
class TestAllocate(unittest.TestCase):
	def test_success(self):
		request = json.dumps(example_request_flat)
		result = json.loads(json_alloc.allocate(request))
		self.assertTrue(result["success"])
	
	def test_fail(self):
		result = json.loads(json_alloc.allocate("qwerty"))
		self.assertEqual(result, {"success":False, "reason":"Invalid JSON"})


if __name__=='__main__':
	unittest.main(verbosity=2) 
