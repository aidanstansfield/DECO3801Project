#    112
# The proof-of-concept allocation, adapted to produce an (incredibly basic) HTML output.

import jinja2
import allocator


# Students to allocate
# In a real application, this would be loaded from a database
# I'm sorry about the names - I was in a hurry.
students     = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]
student_ages = [23, 21, 20, 26, 28, 21, 16, 18, 18, 19, 18, 19, 17, 19]
student_names = [
	"John James",
	"Annie Godfrey",
	"Zach Bishop",
	"Robert Khan",
	"Carlota Henrik",
	"Mora Zebedaios",
	"Matt Randall",
	"Freya Blake",
	"Hannah Boyce",
	"Mike Thomas",
	"Tommy Bishop",
	"Kelly James",
	"Reece James",
	"Gary Greenway",
]
student_preferences = [
	["ui", "networking", "graphics", "gameplay"],
	["graphics", "gameplay"],
	["ui", "gameplay"],
	["ui"],
	["networking", "gameplay"],
	["networking"],
	[],
	["ui", "graphics"],
	["networking", "graphics", "gameplay"],
	["ui", "graphics"],
	["graphics"],
	["gameplay"],
	["ui", "networking", "gameplay"],
	["gameplay"],
]
student_info = {sid:{"name":student_names[sid], "age":student_ages[sid], "preferences":student_preferences[sid]} for sid in students}

# Allocation constraints
# Want exactly one person between ages of 20-30 per team
# Want each team to have shared similar project preferences.
age_constraint = allocator.IntegerCountConstraint("age_constraint", "age", 1, True, allocator.BXY(1,1), True, allocator.BXY(20,30))
preference_constraint = allocator.SubsetSimilarityConstraint("preference constraint", "preferences", 1, True, ("ui", "networking", "graphics", "gameplay"))
constraints = [age_constraint, preference_constraint]

# Allocate
teams = allocator.allocate_teams(2, 3, 4, student_info, constraints)

# Generate HTML document
jinja2_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader('.'),
	autoescape=jinja2.select_autoescape(['html', 'xml'])
)
print(jinja2_env.get_template('display_template.html').render(
	teams = [(num, members, cost) for num, (members, cost) in enumerate(teams.items())],
	student_info = student_info,
))
