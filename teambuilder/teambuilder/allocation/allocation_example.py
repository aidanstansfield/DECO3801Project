# Simple proof-of-concept allocation.
# 14 students are placed into teams based on two constraints.

import os.path
import sys

# PEP366 - don't even ask
if __package__ is None or __package__ == "":
	__package__ = "allocation"
	sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from . import allocator


# Students to allocate
students     = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]
student_ages = [23, 21, 20, 26, 28, 21, 16, 18, 18, 19, 18, 19, 17, 19]
student_preferences = [
	["ui", "networking", "graphics", "gameplay"],
	["graphics", "gameplay"],
	["ui", "gameplay"],
	["ui"],
	["networking", "gameplay"],
	["networking"],
	[],
	["ui", "graphics"],
	["networking", "graphics", "gameplay"],
	["ui", "graphics"],
	["graphics"],
	["gameplay"],
	["ui", "networking", "gameplay"],
	["gameplay"],
]
student_info = {sid:{"age":student_ages[sid], "preferences":student_preferences[sid]} for sid in students}


# Allocation constraints
# Want exactly one person between ages of 20-30 per team
# Want each team to have shared similar project preferences.
age_constraint = allocator.IntegerCountConstraint("age_constraint", "age", 1, True, allocator.BXY(1,1), True, allocator.BXY(20,30))
preference_constraint = allocator.SubsetSimilarityConstraint("preference constraint", "preferences", 1, True, ("ui", "networking", "graphics", "gameplay"))
constraints = [age_constraint, preference_constraint]


# Allocate
teams = allocator.allocate_teams(2, 3, 4, student_info, constraints, progress=True)


# Print results
print()
print()
for team_no, (team, team_cost) in enumerate(teams.items()):
	print(f"Team {team_no}")
	for member in team:
		print(f"sid: {member:3}   age: {student_info[member]['age']:3}   preferences: {', '.join(student_info[member]['preferences'])}")
	print(f"cost:  {team_cost}")
	print()
