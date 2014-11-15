import urllib2
import re

homeURL = 'http://www.ratemyprofessors.com/'

homePage = urllib2.urlopen(homeURL).read()

state_match = re.findall(r'<option value="(\w\w)" >(\w+)</option>', homePage, flags=re.S|re.I|re.M)

if not state_match:
	raise Exception('Could not find state_match')

for state in state_match:
	
	url = "http://www.ratemyprofessors.com/search.jsp?queryoption=SCHOOL&queryBy=schoolLocation&stateselect=%s" % state[0]
	statePage = urllib2.urlopen(url)
	
	if not statePage:
		raise Exception('Could not find statePage!')
	
	statePageRaw = statePage.read()
	
	university_match = re.findall(r'<a href="/campusRatings.jsp\?sid=(\d+)">\s*<span class="name">(.*?)</span>', statePageRaw, flags=re.S|re.I|re.M)
	
	if not university_match:
	
		raise Exception('Could not find university_match!')
	
	for university in university_match:
		
		sid = university[0]
		s_name = university[1]
		
		url = "http://www.ratemyprofessors.com/campusRatings.jsp?sid=%s" % sid
		print url
		university_page = urllib2.urlopen(url)
		
		if not university_page:
			raise Exception('Could not find university_page!')
		
		university_page_raw = university_page.read()
		
		s_name.replace(" ", "+")
		
		url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=%s&sid=%s&queryoption=TEACHER&id=viewprofessors" % (s_name, sid)
		
		professors_page = urllib2.urlopen(url)
		
		if not professors_page:
			
			raise Exception('Could not find professors_page!')
		
		professors_page_raw = professors_page.read()
		
		print professors_page_raw

		professor_id_match = re.findall(r'tid=(\d+)', professors_page_raw, flags=re.S|re.I|re.M)
		
		if not professor_id_match:
			
			raise Exception('Could not find professors_match!')
		
		for professor_id in professor_id_match:
			
			professor_url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % professor_id
			
			professor_page = urllib2.urlopen(professor_url)
			
			if not professor_page:
		
				raise Exception('Could not find professor_page!')
			
			professor_page_raw = professor_page.read()
			
			professor_grade = re.search(r'grade">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
			
			if not professor_grade:
			
				raise Exception('Could not find professor_grade!')
			
			if professor_grade == "0.0":
				
				continue
			
			else:
				
				professor_name = re.search(r'<div class=\"result-name\">(.*?)</span>\s*</div>', professor_page_raw, flags=re.S|re.I|re.M)
				
				if not professor_name:
					
					raise Exception('Could not find professor_name!')
				
				
