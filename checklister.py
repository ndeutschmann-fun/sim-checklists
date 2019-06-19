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
		self.name = str(name)
		self.rows = [ChecklistRow(item,action) for (item,action) in rows.items()]

class Checklist:
	def __init__(self,yaml_input):
		try:
			self.title=str(yaml_input["title"])
			sections_yaml=yaml_input["sections"]
		except KeyError:
			print("YAML input must have a title and a list of sections")
			raise

		try:
			assert isinstance(sections_yaml, dict)
		except AssertionError as e:
			print("YAML 'sections' must be a dict")
			raise

		self.sections=[]

		for name,rows in sections_yaml.items():
			try:
				assert isinstance(rows, dict)
			except AssertionError as e:
				print("Values of 'sections' must be dicts")
				raise
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
		# #TODO DEV remove this debug before pushing
		# import ipdb
		# ipdb.set_trace()
		# #TODO DEV end of debug statement
		checklist = Checklist(yaml_data)

	with open('template.jinja') as file_:
		template = jinja2.Template(file_.read())

	html_output=template.render(checklist=checklist)

	with open(html_filename,"x") as file_:
		file_.write(html_output)



