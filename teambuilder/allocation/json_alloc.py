import json

from . import allocator
from .constraints import * # useful for anything which imports this module 
from .group_size_generator import ImpossibleConstraintsError


# General exception to describe any issues which may arise from
# deserialising a JSON-encoded allocation request.
class InvalidRequestError(Exception):
	def __init__(self, request, message):
		self.request = request
		self.message = message


# Extension to JSONEncoder in order to correctly serialise allocation constraints.
# Not needed for the website, but useful as documentation.
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


# Capture and build constraints from the result of deserialising a
# JSON-encoded allocation request.
def constraint_hook(obj):
	try:
		if obj.get("constr_type") == "IntegerCountConstraint":
			# name, field, priority, should_bool, count_bxy, with_bool, value_bxy
			count_bxy = BXY(*obj["count_bxy"])
			value_bxy = BXY(*obj["value_bxy"])
			return IntegerCountConstraint(obj["name"], obj["field"],obj["priority"],
				obj["should_bool"], count_bxy, obj["with_bool"], value_bxy)
		
		elif obj.get("constr_type") == "SubsetSimilarityConstraint":
			return SubsetSimilarityConstraint(obj["name"], obj["field"],obj["priority"],
				obj["similar_bool"], obj["candidates"])
		
		elif obj.get("constr_type") is not None:
			#TODO will break if anything is called "constr_type"
			raise InvalidRequestError(None, "Invalid constraint JSON")
		
		else:
			return obj
		
	except (KeyError, TypeError):
		name = obj.get("name")
		if name is not None:
			raise InvalidRequestError(None, "Invalid JSON for constraint ({})".format(name))
		else:
			raise InvalidRequestError(None, "Invalid constraint JSON")


# Produce the JSON-encoded result of a successful allocation.
def encode_teams(teams):
	return json.dumps({"success":True, "teams":teams})


# Produce the JSON-encoded result of an unsuccessful allocation.
def encode_failure(exception):
	if isinstance(exception, InvalidRequestError):
		reason = exception.message
	elif isinstance(exception, ImpossibleConstraintsError):
		reason = str(exception)
	else:
		reason = "Something happened"
	return json.dumps({"success":False, "reason":reason})


# Build a valid request 
# Not needed for the website, but useful as documentation.
def encode_request(min_size, ideal_size, max_size, constraints, students):
	return json.dumps({
		"min_size":     min_size,
		"ideal_size":   ideal_size,
		"max_size":     max_size,
		"students":     students,
		"constraints":  constraints},
		cls=ConstraintEncoder)


# Decode an allocation request from a user. This function will validate
# That the request has a valid structure and types, though it won't
# attempt to validate the individual constraints.
def decode_request(request):
	try:
		decoded = json.loads(request, object_hook=constraint_hook)
	except json.decoder.JSONDecodeError:
		raise InvalidRequestError(request, "Invalid JSON")
	except InvalidRequestError as error:
		error.request = request
		raise error
	
	if type(decoded) != dict:
		raise InvalidRequestError(request, "Invalid request")
	
	min_size = decoded.get("min_size")
	if min_size is None or type(min_size) != int:
		raise InvalidRequestError(request, "Invalid minimum size")
	
	ideal_size = decoded.get("ideal_size")
	if ideal_size is None or type(ideal_size) != int:
		raise InvalidRequestError(request, "Invalid ideal size")
	
	max_size = decoded.get("max_size")
	if max_size is None or type(max_size) != int:
		raise InvalidRequestError(request, "Invalid maximum size")
	
	students = decoded.get("students")
	if students is None or type(students) != dict:
		raise InvalidRequestError(request, "Invalid student info")
	
	constraints = decoded.get("constraints")
	if constraints is None:
		constraints = []
	elif type(constraints) != list:
		raise InvalidRequestError(request, "Invalid constraint list")
	
	return min_size, ideal_size, max_size, students, constraints


# Validate a single constraint from an allocation, including whether it
# is applicable to the given student data.
def validate_constraint(request, student_info, constraint):
	if not isinstance(constraint, Constraint):
		raise InvalidRequestError(request, "Invalid constraint")
	
	if constraint.field is None:
		return
	
	for info in student_info.values():
		
		if constraint.field not in info:
			raise InvalidRequestError(request, "Constraint ({}) is on a missing student info field ({})".format(constraint.name, constraint.field))
		
		ctype = constraint.constraint_type
		svalue = info[constraint.field]
		
		if ((ctype == "integer" and type(svalue) != int) or
				(ctype == "option" and type(svalue) != str) or
				(ctype == "subset" and (type(svalue) != list or not all(map(lambda x: type(x)==str, svalue)))) or
				(ctype == "boolean" and type(svalue) != bool)):
			raise InvalidRequestError(request, "Constraint ({}) type ({}) doesn't match student info field ({}) type".format(constraint.name, ctype, constraint.field))


# Validate an allocation request from the user, including constraints and student information
def validate_request(request, min_size, ideal_size, max_size, student_info, constraints): #TODO
	if not min_size <= ideal_size <= max_size:
		raise InvalidRequestError(request, "Invalid group size ordering")
	
	for info in student_info.values():
		if type(info) != dict:
			raise InvalidRequestError(request, "Invalid student data")
	
	for constraint in constraints:
		validate_constraint(request, student_info, constraint)


# Perform the complete deserialise->allocate->serialise process.
def allocate(request):
	try:
		decoded = decode_request(request)
		validate_request(request, *decoded)
		steps = 10**5 #TODO need to control number of annealing steps
		team_data = allocator.allocate_teams(*decoded, steps=steps, progress=False)
		teams = {id:team for id, team in enumerate(team_data.keys())}
		return encode_teams(teams)
	except Exception as e:
		return encode_failure(e)
