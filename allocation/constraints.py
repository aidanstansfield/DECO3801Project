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
		


