import urllib2
import re
try:
	import db_manager
except:
	import os, sys, inspect
	current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	parentdir = os.path.dirname(currentdir)
	sys.path.insert(0, parentdir)
	import db_manager
home_url = "http://registrar.princeton.edu/course-offerings/"

home_page = urllib2.urlopen(home_url)

if not home_page:
	raise Exception('Could not find home_page!')

home_page_raw = home_page.read()
print home_page_raw
study_program_matches = re.findall(r'search_results\.xml\?term=1154&#38;subject=(\w{3})', home_page_raw, flags=re.S|re.I|re.M)

if not study_program_matches:
	raise Exception('Could not find study_program_matches!')
db = db_manager.DatabaseAccess('localhost', 'root','root', 'grades')
db.connect()
for study_program in study_program_matches:
	
	url = "http://registrar.princeton.edu/course-offerings/search_results.xml?term=1154&subject=%s" % study_program
	print url
	study_program_page = urllib2.urlopen(url)
	
	if not study_program_page:
		raise Exception('Could not find study_program_page!')
	
	study_program_page_raw = study_program_page.read()
	
	course_match = re.findall(r'course_details\.xml\?courseid=(\d+)&#38;term=1154', study_program_page_raw, flags=re.S|re.I|re.M)
	
	if not course_match:
		raise Exception('Could not find course_match!')

	for course in course_match:
		url = "http://registrar.princeton.edu/course-offerings/course_details.xml?courseid=%s&term=1154" % course
	
		class_page = urllib2.urlopen(url)
		
		if not class_page:
			raise Exception('Could not find class_page!')
		
		class_page_raw = class_page.read()
		
		crn_match = re.search(r'<tr bgcolor=\"#f0f0f0\">\s*<td><strong>(\d+)</strong></td>', class_page_raw, flags=re.S|re.I|re.M)
		
		if not crn_match:
			raise Exception('Could not find crn_match!')
		if not crn_match:
			raise Exception('Could not find the CRN')
		crn = crn_match.group(1).strip('\n').strip() 
	
		professor_name_match = re.search(r';stopDefAction\(event\);" target="_blank">\s*([^<>]*?)</a>', class_page_raw, flags=re.S|re.I|re.M)
		if not professor_name_match:
			raise Exception('Could not find professor_name_match!')
		
		professor_name = professor_name_match.group(1).replace("\n" , "").replace("\t", "").replace("     ", " ")
		print professor_name
		db.execute_all("UPDATE courses set prof='%s' where crn=%s"%(professor_name, crn))

db.close()
