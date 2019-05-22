#  109

import math
import random

import simanneal

from group_size_generator import determine_group_numbers

def split_teams(students, teams):
	i = 0
	for team_size, team_count in teams.items():
		for _ in range(team_count):
			yield students[i:i+team_size]
			i += team_size

class TeamBuilder(simanneal.Annealer):
	def __init__(self, state, team_sizes, student_info, constraints):
		self.team_sizes = team_sizes
		self.student_info = student_info
		self.constraints = constraints
		super().__init__(state)
	
	# Naive teams sizes, just to keep this prototype simple
	def teams(self):
		return split_teams(self.state, self.team_sizes)
	
	# All moves are just swaps
	def move(self):
		i = random.randrange(0,len(self.state))
		j = random.randrange(0,len(self.state))
		self.state[i], self.state[j] = self.state[j], self.state[i]
	
	# Energy is sum of constraints
	def energy(self):
		cost = 0
		for constraint in self.constraints:
			for team in self.teams():
				cost += constraint.evaluate(team, student_info)
		return cost

class BXY:
	def __init__(self, lower, upper):
		self.lower = lower
		self.upper = upper
	
	def test(self, value):
		return self.lower <= value <= self.upper
	
	def distance(self, value):
		return max(0, self.lower - value, value - self.upper)



class Constraint:
	def __init__(self, name, field, constraint_type, priority):
		self.name = name
		self.field = field
		self.constraint_type = constraint_type
		self.priority = priority
	
	def evaluate(self, team, student_info):
		raise NotImplementedError



class IntegerCountConstraint(Constraint):
	# Each team <should/shouldn’t> have <BXY> members <with/without> [age] <BXY>.
	#                   |                 \-----------------\  |             |
	#                   \------------------------- \        |  \--------\    \------\
	#                                              V        V           V           V
	def __init__(self, name, field, priority, should_bool, count_bxy, with_bool, value_bxy):
		super().__init__(name, field, "integer", priority)
		self.should_bool = should_bool
		self.count_bxy = count_bxy
		self.with_bool = with_bool
		self.value_bxy = value_bxy
	
	def evaluate(self, team, student_info):
		count = 0
		for student in team:
			value = student_info[student][self.field]
			if self.value_bxy.test(value) ^ (not self.with_bool):
				count += 1
		
		if self.should_bool:
			return self.count_bxy.distance(count)
		else:
			return len(team) - self.count_bxy.distance(count)
		



students     = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]
student_ages = [23, 21, 20, 26, 28, 21, 16, 18, 18, 19, 18, 19, 17, 19]
student_info = {sid:{"age":student_ages[sid]} for sid in students}

team_sizes = determine_group_numbers(len(students), 2, 3, 4)

age_constraint = IntegerCountConstraint("age_constraint", "age", 1, True, BXY(1,1), True, BXY(20,30))

tb = TeamBuilder(students, team_sizes, student_info, [age_constraint])
tb.steps = 10**3
tb.copy_strategy = "slice"  # state is a list
result, cost = tb.anneal()
print()
print()
print(result)
print(cost)
print()
for team_no, team in enumerate(split_teams(result, team_sizes)):
	print(f"Team {team_no}")
	for member in team:
		print(f"sid: {member:3}   age: {student_info[member]['age']:3}")
	print(f"cost:  {age_constraint.evaluate(team, student_info)}")
	print()
#print(tb.state)
#print()

