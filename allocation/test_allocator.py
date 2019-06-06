import unittest
import allocator
import constraints


# Tests if list "a" is a permutation of list "b"
def is_permutation(a, b):
	for element in set(a).union(set(b)):
		if a.count(element) != b.count(element):
			return False
	return True


# Make teams based on grouping "True" or "False"
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
	
	# Ensure that the right number of teams are created
	def test_number(self):
		students = range(6)
		sizes = {2:3}
		teams = list(allocator.split_teams(students, sizes))
		self.assertEqual(len(teams), 3)
	
	# Ensure teams are the correct size
	def test_size(self):
		students = range(14)
		sizes = {3:3, 5:1}
		teams = list(allocator.split_teams(students, sizes))
		for team in teams:
			self.assertTrue(len(team) in (3,5))
	
	# Ensure students show up once and only once
	def test_appearance(self):
		students = [object(), object(), object(), object(), object()]
		sizes = {3:2}
		teams = list(allocator.split_teams(students, sizes))
		appeared = []
		for team in teams:
			appeared += team
		self.assertTrue(is_permutation(appeared, students))


class TestTeamBuilderMethods(unittest.TestCase):
	
	# Test that a single "move" of the simulated annealing maintains all elements
	def test_move(self):
		students = ["A", "B", "C", "D", "E"]
		team_sizes = {3:2}
		teambuilder = allocator.TeamBuilder(students, team_sizes, {}, [])
		teambuilder.move()
		appeared = []
		for team in teambuilder.teams():
			appeared += team
		self.assertTrue(is_permutation(appeared, students))
	
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


# Test that complete allocations will occur successfully
# WARNING: allocate_teams() is not deterministic. It's possible, but incredibly unlikely, for this test to fail by chance.
# Also, simanneal doesn't seem to have an option for turning off printing to stderr.
class TestAllocation(unittest.TestCase):
	def test_allocate_teams(self):
		student_info = {"A":True, "B":False, "C":True, "D":False, "E":True, "F":True, "G":False, "H":False}
		teams = allocator.allocate_teams(4, 4, 4, student_info, [DummyConstraint()])
		for team in teams.keys():
			if 'A' in team:
				self.assertTrue(is_permutation(team, ["A", "C", "E", "F"]))
			else:
				self.assertTrue(is_permutation(team, ["B", "D", "G", "H"]))


if __name__=='__main__':
	unittest.main(verbosity=2)
