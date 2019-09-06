# Simple class for working with ranges in constraints
class BXY:
	def __init__(self, lower, upper):
		self.lower = lower
		self.upper = upper
	
	def distance(self, value):
		return max(0, self.lower - value, value - self.upper)
	
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


# A constraint that controls the number of members per-team which match an integer-based condition 
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
			return self.should_tune * self.priority * self.count_bxy.distance(count)
		else:
			return self.shouldnt_tune * self.priority * (len(team) - self.count_bxy.distance(count))


# A constraint requires members of a team to be more/less similar to each other
# in their answers to a "subset" (select multiple values) question 
class SubsetSimilarityConstraint(Constraint):
	similar_tune = 1.0	# tuning values to match influence of different constraints (with the same priority).
	diverse_tune = 1.0
	
	# Each team should have <similar/diverse> [interests].
	#                             |                
	#                             \--------------- \
	#                                              V
	def __init__(self, name, field, priority, similar_bool, candidates):
		super().__init__(name, field, "integer", priority)
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
			return self.diverse_tune * self.priority * (voter_count/len(candidates) - min(votes.values()))


