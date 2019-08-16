# A very hacky mip to test the speed of solve in comparison to current version.
# This needs to be modularized, made neater, and made more generalizable.
# Currently a POC ONLY

from ortools.sat.python import cp_model
from generation.generate_test_data import gen_poc_data
from allocation.group_size_generator import get_group_sizes

fnames = "generation/fnames.txt"
lnames = "generation/lnames.txt"

data = gen_poc_data(100, fnames, lnames)


# =============================================================================
# Data
# =============================================================================
# Modify data for MIP format

print("Formatting data for mip...")

students = list(data.keys())  # represent students by id
preferences = ["ui", "networking", "graphics", "gameplay"]

# Age range constraint settings. Want at least <count> people
# in age range(a1, a2) per group
count = 2
age_range = (20, 30)

age_student = {}
in_age_range = {}
student_preference = {}
for student in students:
    age_student[student] = data[student]['age']
    in_age_range[student] = (age_student[student] >= age_range[0] and
                             age_student[student] <= age_range[1])
    for p in preferences:
        student_preference[student, p] = (p in data[student]['preferences'])

group_sizes = get_group_sizes(len(students), 5, 6, 7)
groups = []
size_group = {}
group_id = 1
for size, num in group_sizes.items():
    for i in range(num):
        groups.append(group_id)
        size_group[group_id] = size
        group_id += 1

print("   ...Done.")

# =============================================================================
# MIP Model
# =============================================================================

print("Forming model...")

# Create the MIP Model
model = cp_model.CpModel()

# VARIABLES
x = {(s, g): model.NewBoolVar('Student {} in group {}'.format(s, g))
     for s in students for g in groups}

v = {(g, p): model.NewIntVar(0, 10**5, 'Votes for {} in group {}'.format(p, g))
     for g in groups for p in preferences}

maxv = {
    g: model.NewIntVar(0, 10**5,
                       'Maximum votes for one pref in group {}'.format(g))
    for g in groups
}

# CONSTRAINTS

# Every student needs to be in exactly one group
for s in students:
    model.Add(sum(x[s, g] for g in groups) == 1)

for g in groups:
    # Ensure group sizes are met in the allocation.
    model.Add(sum(x[s, g] for s in students) == size_group[g])

    # Ensure age range constraints are met
    model.Add(sum(x[s, g]*in_age_range[s] for s in students) >= count)

    # Count votes for each preference
    for p in preferences:
        model.Add(v[g, p] == sum(x[s, g]*student_preference[s, p]
                                 for s in students))
        model.Add(maxv[g] >= v[g, p])  # this is insufficient

print("   ...Done.")

# =============================================================================
# Solve!
# =============================================================================
solver = cp_model.CpSolver()
print("Solving...")
status = solver.Solve(model)
print("   ...Done.")

# =============================================================================
# Model Output
# =============================================================================

if status == cp_model.FEASIBLE:
    print("Success!")
    for g in groups:
        print("\nGroup {}:".format(g))
        for s in students:
            if solver.Value(x[s, g]) == 1:
                print("  " + str(list(data[s].values())))
        for p in preferences:
            print("  " + p + ": " + str(solver.Value(v[g, p])))

        # maximum votes
        print("  maximum votes: ", solver.Value(maxv[g]))
else:
    print("Model infeasible. No solution exists.")
