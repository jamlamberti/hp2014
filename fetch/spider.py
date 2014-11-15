import urllib2
import re
import os
import json
try:
	import db_manager
except:
	import os, inspect, sys
	currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
	parentdir = os.path.dirname(currentdir)
	sys.path.insert(0,parentdir)
	import db_manager

db = db_manager.DatabaseAccess('localhost', 'root', 'root', 'grades')
db.connect()

##homeURL = 'http://www.ratemyprofessors.com/'
##
##homePage = urllib2.urlopen(homeURL).read()
##
##state_match = re.findall(r'<option value="(\w\w)" >(\w+)</option>', homePage, flags=re.S|re.I|re.M)
##
##if not state_match:
##	raise Exception('Could not find state_match')
##
##for state in state_match:
##	
##	url = "http://www.ratemyprofessors.com/search.jsp?queryoption=SCHOOL&queryBy=schoolLocation&stateselect=%s" % state[0]
##	statePage = urllib2.urlopen(url)
##	
##	if not statePage:
##		raise Exception('Could not find statePage!')
##	
##	statePageRaw = statePage.read()
##	
##	university_match = re.findall(r'<a href="/campusRatings.jsp\?sid=(\d+)">\s*<span class="name">(.*?)</span>', statePageRaw, flags=re.S|re.I|re.M)
##	
##	if not university_match:
##	
##		raise Exception('Could not find university_match!')
##	
##	for university in university_match:
##		
##		sid = university[0]
##		s_name = university[1]
##		
##		url = "http://www.ratemyprofessors.com/campusRatings.jsp?sid=%s" % sid
sid = 780
s_name = "Princeton University"

url = "http://www.ratemyprofessors.com/campusRatings.jsp?sid=780"

university_page = urllib2.urlopen(url)

if not university_page:
	raise Exception('Could not find university_page!')

if not os.path.exists(s_name):
	os.makedirs(s_name)

save_path = '~/%s' % s_name

university_page_raw = university_page.read()

html_file = open("%s/princeton_university.txt" % (s_name), "w+")
html_file.write(university_page_raw)
html_file.close()

s_name = s_name.replace(" ", "+")

url = "http://www.ratemyprofessors.com/find/professor/?department=&institution=%s&page=1&queryoption=TEACHER&queryBy=schoolId&sid=%s" % (s_name,  sid)

professors_page = urllib2.urlopen(url)

if not professors_page:
	
	raise Exception('Could not find professors_page!')


professors_page_raw = professors_page.read()
professors_page_json = json.loads(professors_page_raw)

index = 0

while (professors_page_json['remaining'] != 0):
	
	professors = professors_page_json['professors']
	
	for professor in professors:
		teacher_id = professor['tid']
		
		professor_url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % teacher_id
		
		professor_page = urllib2.urlopen(professor_url)
		
		if not professor_page:
	
			raise Exception('Could not find professor_page!')
		
		professor_page_raw = professor_page.read()
		
		professor_grade = re.search(r'grade">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
		
		if not professor_grade:
		
			raise Exception('Could not find professor_grade!')
		
		if professor_grade.group(1) == "0.0":
			
			continue
		
		else:
			
			professor_name_match = re.search(r'<div class=\"result-name\">(.*?</span>)\s*</div>', professor_page_raw, flags=re.S|re.I|re.M)
			if not professor_name:
							
				raise Exception('Could not find professor_name!')

			helpfulness_match = re.search(r'helpfulness</div>\s*<div class=/"rating/">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
			if not helpfulness_match:
				raise Exception('Could not find helpfulness_match!')
			
			clarity_match = re.search(r'clarity</div>\s*<div class=/"rating/">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
			if not clarity_match:
				raise Exception('Could not find clarity_match!')
			
			easiness_match = re.search(r'easiness</div>\s*<div class=/"rating/">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
			if not easiness_match:
				raise Exception('Could not find easiness_match!')

			comments = re.findall(r'<p>\s+([^<>]*?)</p>', professor_page_raw, flags=re.S|re.I|re.M)
			if not comments:
				raise Exception('Could not find comments!')
			
			helpfulness = helpfulness_match.group(1)
			clarity = clarity_match.group(1)
			easiness_match = easiness_match.group(1)
				
			professor_name = professor_name_match.group(1)
			first_name = re.search(r'<span class=\"pfname\">\s*(\w+)</span>', professor_name, flags=re.S|re.I|re.M)
			print professor_name				
			if not first_name:
				continue	
				raise Exception('Could not first_name!')
		
			last_name = re.search(r'<span class=\"plname\">\s*(\w*)</span>', professor_name, flags=re.S|re.I|re.M)
			
			if not last_name:
				continue
				raise Exception('Could not find last_name!')
			
			full_name = first_name.group(1) + " " + last_name.group(1)
			
			print full_name
			sql = "INSERT into preparse VALUES(null, '%s', '%s', %s, %s, %s)"
			args = (full_name,s_name.replace('+', ' '), helpfulness, clarity, easiness)
			print sql%args
			db.execute_all(sql)
			rid = r[0][0]
			args = (rid, random.choice(comments).replace("'", "\\'"))
			sql = "INSERT into comments VALUES(null, %s, '%s')"
			print sql%args
			db.execute_all(sql%args)
	url = "http://www.ratemyprofessors.com/find/professor/?department=&institution=%s&page=1&queryoption=TEACHER&queryBy=schoolId&sid=%s" % (s_name,  sid)

	professors_page = urllib2.urlopen(url)

	if not professors_page:
	
		raise Exception('Could not find professors_page!')


	professors_page_raw = professors_page.read()
	professors_page_json = json.loads(professors_page_raw)

                
        sql = "INSERT into preparse VALUES(null, '%s', '%s', %s, %s, %s)"
        
        args = (full_name, s_name.replace('+', ' '), helpfulness, clarity, easiness) #random.choice(comments).replace("'", "\\'"))
        print sql%args
        db.execute_all(sql%args)
        sql = "SELECT LAST_INSERT_ID()"
        r = db.execute_all(sql)
        rid = r[0][0]
        args = (rid, random.choice(comments).replace("'", "\\'"))
        sql = "INSERT into comments VALUES(null, %s, '%s')"
        print sql%args
        db.execute_all(sql%args)
    break
db.close()
