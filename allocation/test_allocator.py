import unittest
import allocator
import constraints


# Make teams based on grouping "True" and "False"
class DummyConstraint(constraints.Constraint):
	def __init__(self):
		super().__init__("dummy", None, "dummy", 0)
	
	def evaluate(self, team, student_info):
		count = 0
		for member in team:
			if student_info[member]:
				count += 1
		return min(count, len(team)-count)


class TestSplitTeams(unittest.TestCase):
	
	# Ensure teams are the correct size
	def test_size(self):
		students = range(6)
		sizes = {2:3}
		teams = list(allocator.split_teams(students, sizes))
		self.assertEqual(len(teams), 3)
		for team in teams:
			self.assertEqual(len(team), 2)
	
	# Ensure students show up once and only once
	def test_appearance(self):
		students = [object(), object(), object(), object(), object()]
		sizes = {3:2}
		teams = list(allocator.split_teams(students, sizes))
		appeared = []
		for team in teams:
			for student in team:
				self.assertTrue(student in students)
				self.assertFalse(student in appeared)
				appeared.append(student)


class TestTeamBuilderMethods(unittest.TestCase):
	
	# Test that a single "move" of the simulated annealing maintains all elements
	def test_move(self):
		students = ["A", "B", "C", "D", "E"]
		team_sizes = {3:2}
		teambuilder = allocator.TeamBuilder(students, team_sizes, {}, [])
		teambuilder.move()
		appeared = []
		for team in teambuilder.teams():
			for student in team:
				self.assertTrue(student in students)
				self.assertFalse(student in appeared)
				appeared.append(student)
		self.assertEqual(len(appeared), len(students))
	
	# Test that an allocation with no issues has an energy  of zero
	def test_zero_energy(self):
		student_info = {"A":True, "B":True, "C":True, "D":True}
		team_sizes = {4:1}
		teambuilder = allocator.TeamBuilder(student_info.keys(), team_sizes, student_info, [DummyConstraint()])
		self.assertEqual(teambuilder.energy(), 0)
	
	# Test that an allocation with issues spread across multiple teams has the correct energy
	def test_team_energy(self):
		student_info = {"A":True, "B":False, "C":True, "D":False}
		team_sizes = {2:2}
		teambuilder = allocator.TeamBuilder(student_info.keys(), team_sizes, student_info, [DummyConstraint()])
		self.assertEqual(teambuilder.energy(), 2)
	
	# Test that an allocation with multiple issues in one team has the correct energy
	def test_high_energy(self):
		student_info = {"A":True, "B":False, "C":True, "D":False}
		team_sizes = {4:1}
		teambuilder = allocator.TeamBuilder(student_info.keys(), team_sizes, student_info, [DummyConstraint()])
		self.assertEqual(teambuilder.energy(), 4)


if __name__=='__main__':
	unittest.main(verbosity=2)
