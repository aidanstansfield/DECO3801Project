# Example data for use in unit tests.

import json
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
example_teams = {"0":["0","2"], "1":["3","1","4"]}

degrees = ["IT", "CS", "SE"]
preferences = ["ui", "networking", "graphics", "gameplay"]

student_info = {
	"0": {
		"name":        "Alice",
		"age":         18,
		"degree":      "IT",
		"preferences": ["ui", "networking", "graphics", "gameplay"],
		"postgrad":    False},
	"1": {
		"name":        "Bob",
		"age":         19,
		"degree":      "CS",
		"preferences": ["ui", "networking"],
		"postgrad":    False},
	"2": {
		"name":        "Charlie",
		"age":         21,
		"degree":      "CS",
		"preferences": ["ui", "gameplay"],
		"postgrad":    True},
	"3": {
		"name":        "Daniel",
		"age":         22,
		"degree":      "SE",
		"preferences": [],
		"postgrad":    False},
	"4": {
		"name":        "Eric",
		"age":         19,
		"degree":      "IT",
		"preferences": ["networking", "graphics"],
		"postgrad":    False}}

student_info_json = json.dumps(student_info)

age_constraint = constraints.IntegerCountConstraint("age constraint",
	"age", 1, True, constraints.BXY(2,2), True, constraints.BXY(20,30))

age_constraint_flat = {
	"constr_type": "IntegerCountConstraint",
	"name":        "age constraint",
	"field":       "age",
	"priority":    1,
	"should_bool": True,
	"count_bxy":   [2, 2],
	"with_bool":   True,
	"value_bxy":   [20, 30]}

preference_constraint = constraints.SubsetSimilarityConstraint(
	"preference constraint", "preferences", 1,
	True, preferences)

preference_constraint_flat = {
	"constr_type":  "SubsetSimilarityConstraint",
	"name":         "preference constraint",
	"field":        "preferences",
	"priority":     1,
	"similar_bool": True,
	"candidates":   ["ui", "networking", "graphics", "gameplay"]}

example_request_flat = {
	"min_size":    1,
	"ideal_size":  2,
	"max_size":    3,
	"constraints": [age_constraint_flat],
	"students":    student_info}
