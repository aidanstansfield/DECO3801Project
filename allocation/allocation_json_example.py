# Simple proof-of -concept allocation, adapted to load students from a JSON data on stdin. 
# Students are placed into teams based on two constraints.

import json
import os
import sys

import json_alloc
import generation.generate_test_data as gendata


def make_pretty(json_data):
	return json.dumps(json.loads(json_data), sort_keys=True, indent='\t')


# number of students
count = 16
if len(sys.argv) > 1:
	try:
		count = int(sys.argv[1])
	except ValueError:
		pass


# team sizes
min_size   = 3
ideal_size = 4
max_size   = 5


# students to allocate
fnames = os.path.join(os.path.dirname(sys.argv[0]), "generation", "fnames.txt")
lnames = os.path.join(os.path.dirname(sys.argv[0]), "generation", "lnames.txt")
preferences = gendata.DEFAULT_PREFERENCES
students = gendata.gen_students(count, {
			"name": gendata.gen_student_name(fnames, lnames),
			"age": gendata.gen_student_age(17,27),
			"preferences": gendata.gen_student_preferences(preferences),
			})


# Allocation constraints
# Want exactly two people between ages of 20-30 per team
# Want each team to have shared similar project preferences.
age_constraint = json_alloc.IntegerCountConstraint("age_constraint", "age", 1, True, json_alloc.BXY(2,2), True, json_alloc.BXY(20,30))
preference_constraint = json_alloc.SubsetSimilarityConstraint("preference constraint", "preferences", 1, True, ("ui", "networking", "graphics", "gameplay"))
constraints = [age_constraint, preference_constraint]

# serialise
request = json_alloc.encode_request(min_size, ideal_size, max_size, constraints, students)


# print request
print()
print("Allocation request:")
print(make_pretty(request))
print()
print()

# allocate with JSON
response = json_alloc.allocate(request)


# print response
print("Allocation response:")
print(make_pretty(response))

