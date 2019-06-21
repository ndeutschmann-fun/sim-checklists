import sys
from yaml import load, dump
import jinja2

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class ChecklistRow:
	def __init__(self,item,action):
		self.item=str(item)
		self.action=str(action)

class ChecklistSection:
	def __init__(self,name,rows):
		self.name=name
		# rows is a list whose elements are dictionnary with only one entry
		# We get this pair of key,value by converting row.item to a list and
		# accessing the first element
		# This is then turned into a sequence of arguments
		self.rows = [ChecklistRow(*(list(row.items())[0])) for row in rows]

class Checklist:
	def __init__(self,yaml_input):
		try:
			self.title=str(yaml_input["title"])
			sections_yaml=yaml_input["sections"]
		except KeyError:
			print("YAML input must have a title and a list of sections")
			raise

		self.sections=[]

		for name,rows in sections_yaml.items():
			self.sections.append(ChecklistSection(name,rows))


if __name__ == "__main__":
	try:
		assert len(sys.argv)>2
	except AssertionError:
		print("Two arguments needed: YAML input, HTML output")
		raise
	yaml_filename = str(sys.argv[1])
	html_filename = str(sys.argv[2])

	with open(yaml_filename) as file_:
		yaml_data = load(file_,Loader=Loader)
		checklist = Checklist(yaml_data)

	with open('template.jinja') as file_:
		template = jinja2.Template(file_.read())

	html_output=template.render(checklist=checklist)

	with open(html_filename,"x") as file_:
		file_.write(html_output)



