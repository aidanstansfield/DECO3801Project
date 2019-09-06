import json

import allocator
from constraints import * # useful for anything which imports this module 



class ConstraintEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, BXY):
			return list(obj)
			
		elif isinstance(obj, IntegerCountConstraint):
			obj_dict = {"constr_type": "IntegerCountConstraint"}
			for attr in ("name","field","priority","should_bool","count_bxy","with_bool","value_bxy"):
				obj_dict[attr] = getattr(obj, attr)
			return obj_dict
			
		elif isinstance(obj, SubsetSimilarityConstraint):
			obj_dict = {"constr_type": "SubsetSimilarityConstraint"}
			for attr in ("name","field","priority","similar_bool", "candidates"):
				obj_dict[attr] = getattr(obj, attr)
			return obj_dict
			
		else: # fail with TypeError
			return json.JSONEncoder.default(self, obj)


def constraint_hook(obj):
	#try:
		
	if obj.get("constr_type") == "IntegerCountConstraint":
		# name, field, priority, should_bool, count_bxy, with_bool, value_bxy
		count_bxy = BXY(*obj["count_bxy"])
		value_bxy = BXY(*obj["value_bxy"])
		return IntegerCountConstraint(obj["name"], obj["field"],obj["priority"],
			obj["should_bool"], count_bxy, obj["with_bool"], value_bxy)
	
	if obj.get("constr_type") == "SubsetSimilarityConstraint":
		return SubsetSimilarityConstraint(obj["name"], obj["field"],obj["priority"],
			obj["similar_bool"], obj["candidates"])
	
	else:
		return obj
	
	#except KeyError, TypeError:
	#	raise ValueError("Invalid constraint JSON")


def encode_teams(teams):
	return json.dumps({"success":True, "teams":teams})


def encode_request(min_size, ideal_size, max_size, constraints, students):
	return json.dumps({
		"min_size":     min_size,
		"ideal_size":   ideal_size,
		"max_size":     max_size,
		"students":     students,
		"constraints":  constraints},
		cls=ConstraintEncoder)


def decode_request(request):
	decoded = json.loads(request, object_hook=constraint_hook)
	min_size = decoded["min_size"]
	ideal_size = decoded["ideal_size"]
	max_size = decoded["max_size"]
	constraints = decoded["constraints"]
	students = decoded["students"]
	return min_size, ideal_size, max_size, constraints, students


def allocate(request):
	min_size, ideal_size, max_size, constraints, student_info = decode_request(request)
	steps = 10**5 #TODO need to control number of annealing steps
	team_data = allocator.allocate_teams(min_size, ideal_size, max_size, student_info, constraints, steps=steps, progress=False)
	teams = {id:team for id, team in enumerate(team_data.keys())}
	return encode_teams(teams)
