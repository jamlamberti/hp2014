import random
try:
    import db_manager
except:
    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    import db_manager

courses_by_dept = {}
all_courses = []
db = db_manager.DatabaseAccess('localhost', 'root', 'root', 'grades')
db.connect()
sql = "SELECT id, course, prof from courses"
r = db.execute_all(sql)
for row in r:
    cid = row[0]
    course = row[1].split()[0] # Get the department
    prof = row[2]
    #print prof
    sql = "SELECT overall from postparse where id='%s'"
    #print sql%prof
    r = db.execute_all(sql%prof)
    #print r
    overall = r[0][0]
    if course not in courses_by_dept:
        courses_by_dept[course] = []
    courses_by_dept[course].append([cid, prof, overall])
    all_courses.append([cid, prof, overall])

# Normalize!
total = 0
for i in range(len(all_courses)):
    cid, prof, overall = all_courses[i]
    total += overall
    all_courses[i] = [cid, prof, total]
max_all = total
#print max_all
depts = courses_by_dept.keys()
for key in depts:
    total = 0
    for i in range(len(courses_by_dept[course])):
        cid, prof, overall = courses_by_dept[course][i]
        total+= overall
        courses_by_dept[course][i] = [cid, prof, total]
# Compute statistics for each prof.
#print all_courses
#print courses_by_dept
courses_per_semester = 6
in_major = 4
out_of_major = 2
ugrads = 5000
schedules = []
for i in range(ugrads):
    major = random.choice(courses_by_dept.keys())
    classes = []
    for j in range(in_major):
        classes.append(random.choice(courses_by_dept[major]))
    for j in range(out_of_major):
        classes.append(random.choice(all_courses))
    schedules.append([major, classes])
print schedules

