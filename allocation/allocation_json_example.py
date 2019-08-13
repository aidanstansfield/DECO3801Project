# Simple proof-of -concept allocation, adapted to load students from a JSON data on stdin. 
# Students are placed into teams based on two constraints.

import json
import sys

import allocator


# Students to allocate
data_str = sys.stdin.read()
student_info = json.loads(data_str)


# Allocation steps
steps = allocator.ANNEAL_STEPS
if len(sys.argv) > 1:
	try:
		steps = int(sys.argv[1])
	except ValueError:
		pass


# Allocation constraints
# Want exactly two people between ages of 20-30 per team
# Want each team to have shared similar project preferences.
age_constraint = allocator.IntegerCountConstraint("age_constraint", "age", 1, True, allocator.BXY(2,2), True, allocator.BXY(20,30))
preference_constraint = allocator.SubsetSimilarityConstraint("preference constraint", "preferences", 1, True, ("ui", "networking", "graphics", "gameplay"))
constraints = [age_constraint, preference_constraint]


# Allocate
teams = allocator.allocate_teams(3, 4, 5, student_info, constraints, steps=steps, progress=True)


# Print results
print()
print()
for team_no, (team, team_cost) in enumerate(teams.items()):
	print(f"Team {team_no}")
	for member in team:
		print(f"sid: {member:3}   age: {student_info[member]['age']:3}   preferences: {', '.join(student_info[member]['preferences'])}")
	print(f"cost:  {team_cost}")
	print()

