import urllib2
import re
import json
import random
import os

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

professors_page = urllib2.urlopen(url)
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
                        if not professor_name_match: 
                                raise Exception('Could not find professor_name!')

                        helpfulness_match = re.search(r'helpfulness</div>\s*<div class=\"rating\">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
                        if not helpfulness_match:
                                helpfulness_match = None
                                continue
                                raise Exception('Could not find helpfulness_match!')

                        clarity_match = re.search(r'clarity</div>\s*<div class=\"rating\">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
                        if not clarity_match:
                                clarity_match = None
                                continue
                                raise Exception('Could not find clarity_match!')

                        easiness_match = re.search(r'easiness</div>\s*<div class=\"rating\">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
                        if not easiness_match:
                                easiness_match = None
                                continue
                                raise Exception('Could not find easiness_match!')
			
			professor_name_match = professor_name_match.group(1)
                        comments = re.findall(r'<p>\s+([^<>]*?)</p>', professor_page_raw, flags=re.S|re.I|re.M)
                        first_name = re.search(r'<span class=\"pfname\">\s*(\w+)</span>', professor_name_match, flags=re.S|re.I|re.M)
	                #print professor_name                
	                if not first_name:
	                    continue    
	                    raise Exception('Could not first_name!')
	            
	                last_name = re.search(r'<span class=\"plname\">\s*(\w*)</span>', professor_name_match, flags=re.S|re.I|re.M)
	                
	                if not last_name:
	                    continue
	                    raise Exception('Could not find last_name!')
	                
	                full_name = first_name.group(1) + " " + last_name.group(1)


			if not comments:
                                comments = None
                                continue
                                raise Exception('Could not find comments!')
                        if helpfulness_match is None:
                            helpfulness = str(int(random.random()*50)/10.0)
                        else:
                            helpfulness = helpfulness_match.group(1)
                        if clarity_match is None:
                            clarity = str(int(random.random()*50)/10.0)
                        else:
                            clarity = clarity_match.group(1)

                        if easiness_match is None:
                            easiness = str(int(random.random()*50)/10.0)
                        else:
                            easiness = easiness_match.group(1)
			
			print "helpfullness: %s"  % helpfulness
			print "clarity: %s" % clarity
			print "easiness: %s" % easiness
        
        		sql = "INSERT into preparse VALUES(null, '%s', '%s', %s, %s, %s)"

                 	args = (full_name, s_name.replace('+', ' '), helpfulness, clarity, easiness) #random.choice(comments).replace("'", "\\'"))
                 	print sql%args
                 	db.execute_all(sql%args)
                 	sql = "SELECT LAST_INSERT_ID()"
                 	r = db.execute_all(sql)
                 	rid = r[0][0]
                 	for i in comments:
                 	    args = (rid, i.strip().replace("'", "\\'"))
                 	    sql = "INSERT into comments VALUES(null, %s, '%s')"
                 	    print sql%args
                 	    db.execute_all(sql%args)


	index += 1
        url = "http://www.ratemyprofessors.com/find/professor/?department=&institution=%s&page=%s&queryoption=TEACHER&queryBy=schoolId&sid=%s" % (s_name, index, sid)

        professors_page = urllib2.urlopen(url)

        if not professors_page:

                raise Exception('Could not find professors_page!')


        professors_page_raw = professors_page.read()
        professors_page_json = json.loads(professors_page_raw)


        db.close()

#homeURL = 'http://www.ratemyprofessors.com/'
#
#homePage = urllib2.urlopen(homeURL).read()
#
#state_match = re.findall(r'<option value="(\w\w)" >(\w+)</option>', homePage, flags=re.S|re.I|re.M)
#
#if not state_match:
#    raise Exception('Could not find state_match')
#
#for state in state_match:
#    
#    url = "http://www.ratemyprofessors.com/search.jsp?queryoption=SCHOOL&queryBy=schoolLocation&stateselect=%s" % state[0]
#    statePage = urllib2.urlopen(url)
#    
#    if not statePage:
#        raise Exception('Could not find statePage!')
#    
#    statePageRaw = statePage.read()
#    
#    university_match = re.findall(r'<a href="/campusRatings.jsp\?sid=(\d+)">\s*<span class="name">(.*?)</span>', statePageRaw, flags=re.S|re.I|re.M)
#    
#    if not university_match:
#    
#        raise Exception('Could not find university_match!')
#    
#    for university in university_match:
#        
#        sid = university[0]
#        s_name = university[1]
#        
#        url = "http://www.ratemyprofessors.com/campusRatings.jsp?sid=%s" % sid
#        university_page = urllib2.urlopen(url)
#        
#        if not university_page:
#            raise Exception('Could not find university_page!')
#        
#        university_page_raw = university_page.read()
#        
#        s_name = s_name.replace(" ", "+")
#        
#        url = "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=%s&sid=%s&queryoption=TEACHER&id=viewprofessors" % (s_name, sid)
#        
#        professors_page = urllib2.urlopen(url)
#        
#        if not professors_page:
#            
#            raise Exception('Could not find professors_page!')
#        
#        professors_page_raw = professors_page.read()
#        
#        professor_id_match = re.findall(r'tid=(\d+)', professors_page_raw, flags=re.S|re.I|re.M)
#        
#        if not professor_id_match:
#            
#            raise Exception('Could not find professors_match!')
#        print "Found professor ids"
#        for professor_id in professor_id_match:
#            
#            professor_url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=%s" % professor_id
#            
#            professor_page = urllib2.urlopen(professor_url)
#            
#            if not professor_page:
#        
#                raise Exception('Could not find professor_page!')
#            
#            professor_page_raw = professor_page.read()
#            
#            professor_grade = re.search(r'grade">(\d\.\d)</div>', professor_page_raw, flags=re.S|re.I|re.M)
#            
#            if not professor_grade:
#            
#                raise Exception('Could not find professor_grade!')
#            
#            if professor_grade.group(1) == "0.0":
#                
#                continue
#            
#            else:
#                
#                professor_name = re.search(r'<div class=\"result-name\">(.*?</span>)\s*</div>', professor_page_raw, flags=re.S|re.I|re.M)
#                
#                if not professor_name:
#                                
#                    raise Exception('Could not find professor_name!')
#
#                professor_name = professor_name.group(1)
#                first_name = re.search(r'<span class=\"pfname\">\s*(\w+)</span>', professor_name, flags=re.S|re.I|re.M)
#                #print professor_name                
#                if not first_name:
#                    continue    
#                    raise Exception('Could not first_name!')
#            
#                last_name = re.search(r'<span class=\"plname\">\s*(\w*)</span>', professor_name, flags=re.S|re.I|re.M)
#                
#                if not last_name:
#                    continue
#                    raise Exception('Could not find last_name!')
#                
#                full_name = first_name.group(1) + " " + last_name.group(1)
#
#                print full_name
#                
#                helpfulness = int(random.random()*50)
#                clarity = int(random.random()*50)
#                easiness = int(random.random()*50)
#                sql = "INSERT into preparse VALUES(null, '%s', '%s', %s, %s, %s)"
#                comments = [
#                    "Worst professor I have ever had a Lehigh. I didn't learn anything from Haller, and I am normally a straight A student. This class was the biggest waste of time and credit hours, I wish that another teacher was available for the same course.",
#                    " The only way to pass his class is to go to his office hours. It's pretty ridiculous that students HAVE to do that. The average for the midterm is extremely low, but he only cares about the final. Homework is required in every single lecture. Make sure he knows your name and go to his office hours. He's mean. ",
#                    " Literally all he cares about is money and drinking scotch on the porch of his big house with a long ass driveway. Trust me, he'll tell you all about it every class.",
#                    " Great professor who is always willing to help. Jokes with students but takes his class very seriously. He knows what he is doing and just wants you to know what your doing. His biggest concern is that you get a job and he wants to teach you everything he knows in order to accomplish that. That said, his class his hard. Make sure he knows your name. ",
#                    " Wish there were other options for professors teaching the same courses as he. ",
#                    " One of the best in the ECE department. His lectures are not only very entertaining at times, but also very good at explaining the material. He has high expectations but that means most students learn a lot and do well. ",
#                    " Haller is just amazing. At the end in senior project, he really makes sure you pull together everything you've learned in ECE. And above that he's very dedicated to see all his students succeed in class and in life! ",
#                    " By far THE BEST professor I've ever had!! His classes are hard but he makes them extremely fun to be at! As long as you're dedicated, he will be extremely helpful to you. Most students finish his course with an A, but that's because he expects only the best! ",
#                    " Best prof ever! Lectures are extremely fun and entertaining! Topics covered are very hard, but he makes them easier to understand. One of the best ECE prof out there! And remember to model your circuits! "]
#
#
#
#
#                
#                args = (full_name, s_name.replace('+', ' '), helpfulness, clarity, easiness) #random.choice(comments).replace("'", "\\'"))
#                print sql%args
#                db.execute_all(sql%args)
#                sql = "SELECT LAST_INSERT_ID()"
#                r = db.execute_all(sql)
#                rid = r[0][0]
#                args = (rid, random.choice(comments).replace("'", "\\'"))
#                sql = "INSERT into comments VALUES(null, %s, '%s')"
#                print sql%args
#                db.execute_all(sql%args)
#    break
#db.close()import urllib2
