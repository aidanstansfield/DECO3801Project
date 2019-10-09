# This file defines classes for representing constraints
# (besides group size) in an allocation.

import math


def team_mean(team, student_info, field):
	return sum(student_info[student][field] for student in team) / len(team)

def team_stdev(team, student_info, field):
	team_average = team_mean(team, student_info, field)
	sqdiffs = sum((student_info[student][field] - team_average)**2 for student in team)
	return math.sqrt(sqdiffs / (len(team)-1))


# Simple class for working with ranges in constraints
class BXY:
	def __init__(self, lower, upper):
		self.lower = lower
		self.upper = upper
	
	# returns the width of the interval represented by the BXY
	def width(self):
		return self.upper - self.lower + 1
	
	# returns how far outside the BXY a value is, or 0 if the value is inside
	def distance(self, value):
		return max(0, self.lower - value, value - self.upper)
	
	# returns how many widths outside of the BXY a value is
	def scaled_distance(self, value):
		return self.distance(value) / self.width()
	
	# returns how far inside the BXY a value is, or 0 if the value is outside
	def inclusion(self, value):
		return max(0, min(value - self.lower + 1, self.upper - value + 1))
	
	# returns what fraction of a radii inside of the BXY a value is
	def scaled_inclusion(self, value):
		radius = math.ceil(self.width() / 2)
		return self.inclusion(value) / radius
	
	def __contains__(self, item):
		return self.lower <= item <= self.upper
	
	def __len__(self):
		return 2
	
	def __getitem__(self, key):
		if key == 0:
			return self.lower
		elif key == 1:
			return self.upper
		else:
			raise IndexError


# ABC for all constraints
class Constraint:
	def __init__(self, name, field, constraint_type, priority):
		self.name = name
		self.field = field
		self.constraint_type = constraint_type
		self.priority = priority
	
	# Returns a "badness" score for the tested team
	def evaluate(self, team, student_info):
		raise NotImplementedError


# A constraint that controls the number of members per-team which match an integer-based condition.
class IntegerCountConstraint(Constraint):
	should_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	shouldnt_tune = 1.0
	
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
			if (value in self.value_bxy) ^ (not self.with_bool):
				count += 1
		
		if self.should_bool:
			return self.should_tune * self.priority * self.count_bxy.scaled_distance(count)
		else:
			return self.shouldnt_tune * self.priority * self.count_bxy.scaled_inclusion(count)


# A constraint that controls the team-wide average of some property.
class IntegerAverageConstraint(Constraint):
	should_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	shouldnt_tune = 1.0
	
	# Each team <should/shouldn’t> have an average [age] <BXY>.
	#                   |                                  |
	#                   \--------------------------\       \----\
	#                                              V            V
	def __init__(self, name, field, priority, should_bool, average_bxy):
		super().__init__(name, field, "integer", priority)
		self.should_bool = should_bool
		self.average_bxy = average_bxy
	
	def evaluate(self, team, student_info):
		mean = team_mean(team, student_info, self.field)
		if self.should_bool:
			return self.should_tune * self.priority * self.average_bxy.scaled_distance(mean)
		else:
			return self.shouldnt_tune * self.priority * self.average_bxy.scaled_inclusion(mean)


# A constraint that controls the team-wide average of some property.
class IntegerSimilarityConstraint(Constraint):
	tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	
	# Each team should have <similar/diverse> [age].
	#                               |
	#                               \--------------\
	#                                              V
	def __init__(self, name, field, priority, similar_bool):
		super().__init__(name, field, "integer", priority)
		self.similar_bool = similar_bool
	
	def evaluate(self, team, student_info):
		stddev = team_stdev(team, student_info, self.field)
		if self.similar_bool:
			return self.tune * self.priority * stddev
		else:
			min_val = min(student_info[student][self.field] for student in student_info)
			max_val = max(student_info[student][self.field] for student in student_info)
			max_std = (max_val - min_val) / math.sqrt(2)
			return self.tune * self.priority * (max_std - stddev)


# A constraint requires members of a team to be more/less similar to each other
# in their answers to a "subset" (select multiple values) question
class SubsetSimilarityConstraint(Constraint):
	similar_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	diverse_tune = 1.0
	
	# Each team should have <similar/diverse> [interests].
	#                             |                
	#                             \----------------\
	#                                              V
	def __init__(self, name, field, priority, similar_bool, candidates):
		super().__init__(name, field, "subset", priority)
		self.similar_bool = similar_bool
		self.candidates = candidates
	
	def evaluate(self, team, student_info):
		votes = {candidate:0 for candidate in self.candidates}
		voter_count = 0
		
		# Collect votes
		for student in team:
			num_votes = len(student_info[student][self.field])
			if num_votes > 0:
				voter_count += 1
				for candidate in student_info[student][self.field]:
					votes[candidate] += 1/num_votes
		
		if self.similar_bool:
			return self.similar_tune * self.priority * (voter_count - max(votes.values()))
		else:
			return self.diverse_tune * self.priority * (voter_count/len(self.candidates) - min(votes.values()))


