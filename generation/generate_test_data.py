import json
import random
import sys


def gen_student_id():
	generated = set()
	length = 8
	while True:
		digits = [4]
		for _ in range(length-2):
			digits.append(random.randrange(10))
		check = (9*digits[0]+7*digits[1]+3*digits[2]+9*digits[3]+7*digits[4]+3*digits[5]+9*digits[6]) % 10
		fake_check = (check + 1) % 10 # intentionally generate invalid student IDs
		digits.append(fake_check)
		new_id = ''.join([str(i) for i in digits])
		if new_id not in generated:
			generated.add(new_id)
			yield new_id


def gen_student_name(fn_filename, ln_filename):
	first_names = []
	last_names = []
	with open(fn_filename, "r") as fn_file:
		for line in fn_file:
			if line != '\n' and line[0] != '#':
				first_names.append(line.strip('\n'))
	with open(ln_filename, "r") as ln_file:
		for line in ln_file:
			if line != '\n' and line[0] != '#':
				last_names.append(line.strip('\n'))
	while True:
		yield f"{random.choice(first_names)} {random.choice(last_names)}"


def gen_student_age(lower_bound, upper_bound):
	while True:
		yield random.randint(lower_bound, upper_bound)


def gen_student_preferences(preferences):
	while True:
		student_preferences = []
		for preference, chance in preferences.items():
			if random.random() < chance:
				student_preferences.append(preference)
		yield student_preferences


def gen_students(count, other_gens):
	id_gen = gen_student_id()
	students = {}
	for _ in range(count):
		student = {}
		for field, generator in other_gens.items():
			student[field] = generator.__next__()
		students[id_gen.__next__()] = student
	return students


count = 16
if len(sys.argv) > 1:
	try:
		count = int(sys.argv[1])
	except ValueError:
		pass

preferences = {
	"ui":         0.2,
	"networking": 0.25,
	"graphics":   0.3,
	"gameplay":   0.4,
	}

students = gen_students(count, {
		"name": gen_student_name("fnames.txt", "lnames.txt"),
		"age": gen_student_age(17,27),
		"preferences": gen_student_preferences(preferences),
		})

print(json.dumps(students))
