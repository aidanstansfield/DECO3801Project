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
	should_tune = 1.0
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
			if self.value_bxy.test(value) ^ (not self.with_bool):
				count += 1
		
		if self.should_bool:
			return self.should_tune * self.priority * self.count_bxy.distance(count)
		else:
			return self.shouldnt_tune * self.priority * (len(team) - self.count_bxy.distance(count))


class SubsetSimilarityConstraint(Constraint):
	similar_tune = 1.0
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


