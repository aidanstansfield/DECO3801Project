from generate_test_data import *

from operator import attrgetter
import random


def gen_student_role():
	while True:
		yield random.choice(["developer","designer"])





if __name__ == "__main__":
	count = 20
	if len(sys.argv) > 1:
		try:
			count = int(sys.argv[1])
		except ValueError:
			pass
	
	fnames = os.path.join(os.path.dirname(sys.argv[0]), "fnames.txt")
	lnames = os.path.join(os.path.dirname(sys.argv[0]), "lnames.txt")
	
	students = gen_students(count, {
			"name": gen_student_name(fnames, lnames),
			"role": gen_student_role(),
			})
	
	print("id, name, role")
	for sid, student in students.items():
		#print(','.join([student["id"], student["name"], student["role"]]))
		print(sid +', "'+ student["name"] +'", '+ student["role"])
