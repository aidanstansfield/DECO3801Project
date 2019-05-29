#  109

import allocator


students     = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]
student_ages = [23, 21, 20, 26, 28, 21, 16, 18, 18, 19, 18, 19, 17, 19]
student_info = {sid:{"age":student_ages[sid]} for sid in students}

age_constraint = allocator.IntegerCountConstraint("age_constraint", "age", 1, True, allocator.BXY(1,1), True, allocator.BXY(20,30))
constraints = [age_constraint]

teams = allocator.allocate_teams(2, 3, 4, student_info, constraints)


print()
print()
for team_no, (team, team_cost) in enumerate(teams.items()):
	print(f"Team {team_no}")
	for member in team:
		print(f"sid: {member:3}   age: {student_info[member]['age']:3}")
	print(f"cost:  {team_cost}")
	print()

