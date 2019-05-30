import math
import random

import simanneal

from constraints import *
from group_size_generator import get_group_sizes


ANNEAL_STEPS = 1000


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


def allocate_teams(min_size, ideal_size, max_size, student_info, constraints):
	students = list(student_info.keys())
	team_sizes = get_group_sizes(len(students), min_size, ideal_size, max_size)
	allocator = TeamBuilder(students, team_sizes, student_info, constraints)
	allocator.steps = ANNEAL_STEPS
	allocator.copy_strategy = "slice"  # state is a list
	allocator.anneal()
	return {tuple(team):allocator.team_energy(team) for team in allocator.teams()}
