import math
import random

import simanneal

from constraints import *
from group_size_generator import get_group_sizes


# Number of annealing steps to perform.
#This should be set in some intelligent way, rather than just using a constant.
ANNEAL_STEPS = 10**4


# Given a list of students and a {size->number} description of desired team sizes
# yield an iterator over subsets of the students that form groups of those sizes.
def split_teams(students, teams):
	i = 0
	for team_size, team_count in teams.items():
		for _ in range(team_count):
			yield students[i:i+team_size]
			i += team_size


# simanneal derived class, used for all allocations
class TeamBuilder(simanneal.Annealer):
	def __init__(self, state, team_sizes, student_info, constraints):
		self.team_sizes = team_sizes
		self.student_info = student_info
		self.constraints = constraints
		super().__init__(state)
	
	# Produce an iterator over the current state of the teams 
	def teams(self):
		return split_teams(self.state, self.team_sizes)
	
	# All moves are just swaps
	def move(self):
		i = random.randrange(0,len(self.state))
		j = random.randrange(0,len(self.state))
		self.state[i], self.state[j] = self.state[j], self.state[i]
	
	# Calculate cost of a single team - sum of constraints
	def team_energy(self, team):
		cost = 0
		for constraint in self.constraints:
			cost += constraint.evaluate(team, self.student_info)
		return cost
	
	# Energy is sum of squares of team costs
	# Sum of squares ensures that imperfections are spread out across the class, rather than making one "bad" team.s
	def energy(self):
		cost = 0
		for team in self.teams():
			cost += self.team_energy(team) ** 2
		return cost


# Given a dictionary of information about students and a list of constraints, perform an allocation.
def allocate_teams(min_size, ideal_size, max_size, student_info, constraints):
	students = list(student_info.keys())
	team_sizes = get_group_sizes(len(students), min_size, ideal_size, max_size)
	allocator = TeamBuilder(students, team_sizes, student_info, constraints)
	allocator.steps = ANNEAL_STEPS
	allocator.copy_strategy = "slice"  # state is a list
	allocator.anneal()
	return {tuple(team):allocator.team_energy(team) for team in allocator.teams()}
