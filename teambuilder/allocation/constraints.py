# This file defines classes for representing constraints
# (besides group size) in an allocation.

import math


# Calculate the mean value of some property in a team
def team_mean(team, student_info, field):
	return sum(student_info[student][field] for student in team) / len(team)

# Calculate the standard deviation of some property in a team
def team_stdev(team, student_info, field):
	team_average = team_mean(team, student_info, field)
	sqdiffs = sum((student_info[student][field] - team_average)**2 for student in team)
	return math.sqrt(sqdiffs / (len(team)-1))

# Return all members of a team who do / do not meet some condition
def team_filter(team, student_info, field, with_bool, function):
	return [student for student in team if function(student_info[student][field]) ^ (not with_bool)]


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
		count = len(team_filter(team, student_info, self.field, self.with_bool, lambda x: x in self.value_bxy))
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


# A constraint that controls how close teams are to the global average of some property.
class IntegerGlobalAverageConstraint(Constraint):
	tune = 1.0	# tuning value to match influence of different constraints (with the same priority).
	
	# All teams should have similar average [age].
	def __init__(self, name, field, priority):
		super().__init__(name, field, "integer", priority)
	
	def evaluate(self, team, student_info):
		global_mean = team_mean(student_info.keys(), student_info, self.field)
		mean = team_mean(team, student_info, self.field)
		return self.tune * self.priority * abs(global_mean - mean)


# A constraint that controls the number of members per-team which selected a particular option
# "candidates" is a list of valid answers to the question
class OptionCountConstraint(Constraint):
	should_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	shouldnt_tune = 1.0
	
	# Each team <should/shouldn’t> have <BXY> members <with/without> [degree] <VALUE>.
	#                   |                 \-----------------\   |                |
	#                   \------------------------- \        |   \--------\       \--\
	#                                              V        V            V          V
	def __init__(self, name, field, priority, should_bool, count_bxy, with_bool, selection, candidates):
		super().__init__(name, field, "option", priority)
		self.should_bool = should_bool
		self.count_bxy = count_bxy
		self.with_bool = with_bool
		self.selection = selection
		self.candidates = candidates
	
	def evaluate(self, team, student_info):
		count = len(team_filter(team, student_info, self.field, self.with_bool, lambda x: x == self.selection))
		if self.should_bool:
			return self.should_tune * self.priority * self.count_bxy.scaled_distance(count)
		else:
			return self.shouldnt_tune * self.priority * self.count_bxy.scaled_inclusion(count)


# A constraint which requires members of a team to be more/less similar
# to each other in their answers to an "option" (select one of) question
# "candidates" is a list of valid answers to the question
class OptionSimilarityConstraint(Constraint):
	similar_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	diverse_tune = 1.0
	
	# Each team should have <similar/diverse> [degree].
	#                              |
	#                              \---------------\
	#                                              V
	def __init__(self, name, field, priority, similar_bool, candidates):
		super().__init__(name, field, "option", priority)
		self.similar_bool = similar_bool
		self.candidates = candidates
	
	def evaluate(self, team, student_info):
		votes = {candidate:0 for candidate in self.candidates}
		
		# Collect votes
		for student in team:
			choice = student_info[student][self.field]
			votes[choice] += 1
		
		if self.similar_bool:
			return self.similar_tune * self.priority * (len(team) - max(votes.values()))
		else:
			return self.diverse_tune * self.priority * (len(team)/len(self.candidates) - min(votes.values()))


# A constraint that controls the number of members per-team which selected a particular choice
# "candidates" is a list of valid answers to the question
class SubsetCountConstraint(Constraint):
	should_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	shouldnt_tune = 1.0
	
	# Each team <should/shouldn’t> have <BXY> members <with/without> [interests] <VALUE>.
	#                   |                 \-----------------\   |                   |
	#                   \------------------------- \        |   \--------\          |
	#                                              V        V            V          V
	def __init__(self, name, field, priority, should_bool, count_bxy, with_bool, selection, candidates):
		super().__init__(name, field, "subset", priority)
		self.should_bool = should_bool
		self.count_bxy = count_bxy
		self.with_bool = with_bool
		self.selection = selection
		self.candidates = candidates
	
	def evaluate(self, team, student_info):
		count = len(team_filter(team, student_info, self.field, self.with_bool, lambda x: self.selection in x))
		if self.should_bool:
			return self.should_tune * self.priority * self.count_bxy.scaled_distance(count)
		else:
			return self.shouldnt_tune * self.priority * self.count_bxy.scaled_inclusion(count)


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


# A constraint that controls the number of members per-team with some boolean criteria
# "candidates" is a list of valid answers to the question
class BooleanCountConstraint(Constraint):
	should_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	shouldnt_tune = 1.0
	
	# Each team <should/shouldn’t> have <BXY> members <with/without> [postgraduate].
	#                   |                 \-----------------\   |
	#                   \------------------------- \        |   \--------\
	#                                              V        V            V
	def __init__(self, name, field, priority, should_bool, count_bxy, with_bool):
		super().__init__(name, field, "boolean", priority)
		self.should_bool = should_bool
		self.count_bxy = count_bxy
		self.with_bool = with_bool
	
	def evaluate(self, team, student_info):
		count = len(team_filter(team, student_info, self.field, self.with_bool, lambda x: x))
		if self.should_bool:
			return self.should_tune * self.priority * self.count_bxy.scaled_distance(count)
		else:
			return self.shouldnt_tune * self.priority * self.count_bxy.scaled_inclusion(count)
