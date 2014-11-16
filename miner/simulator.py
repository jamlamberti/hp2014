import random
try:
    import db_manager
except:
    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    import db_manager
import datetime
today = datetime.datetime.today().weekday()
if today == 0:
    monday = datetime.datetime.today()
else:
    monday = datetime.date.today()-datetime.timedelta(days=today)
td1 = datetime.timedelta(days=1)
tuesday = monday+td1
wednesday = tuesday + td1
thursday = wednesday + td1
friday = thursday + td1
saturday = friday + td1
sunday = monday - td1
def d2date(d):
    temp = None
    if d == 'M':
        temp = monday
    elif d == 'T':
        temp = tuesday
    elif d == 'W':
        temp = wednesday
    elif d == 'Th':
        temp = thursday
    else:
        temp = friday
    return temp.strftime("%Y-%m-%d")
def weighted_random(a):
    max_val = a[-1][0]
    rand = random.random()*max_val
    for i in a:
        if i[0] > rand:
            return i
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
    try:
        overall = r[0][0]
    except:
        overall = int(random.random()*100)
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
courses_per_semester = 4
in_major = 3
out_of_major = 1
ugrads = 5000
schedules = []
for i in range(ugrads):
    major = random.choice(courses_by_dept.keys())
    classes = []
    for j in range(in_major):
        #classes.append(random.choice(courses_by_dept[major]))
        classes.append(weighted_random(courses_by_dept[major]))
    for j in range(out_of_major):
        #classes.append(random.choice(all_courses))
        classes.append(weighted_random(all_courses))
    schedules.append([major, classes])
#print schedules
major = "COS"
schedule = []
for i in range(7):
    c = weighted_random(courses_by_dept[major])
    while c[0] in schedule:
        c = weighted_random(courses_by_dept[major])
    schedule.append(c)
for i in range(3):
    c = weighted_random(all_courses)
    while c[0] in schedule:
        c = weighted_random(all_courses)
    schedule.append(c)
f = open('frontend/public/data.json', 'w')
# Convert schedule to JSON
for i in schedule:
    sql = "SELECT * from courses where id=%s"%i[0]
    r = db.execute_all(sql)
    cid, crn, course, title, dist, sect, days, t, prof = r[0]
    sql = "SELECT * from postparse where prof='%s'"%prof
    if prof is None:
        prof = ""
    r = db.execute_all(sql)
    try:
        difficulty = int(r[0][0])
    except:
        difficulty = int(random.random()*50)
        try:
            startTime, endTime = t.split('-')
            startTime = startTime.strip().upper()
            endTime = endTime.strip().upper()
            startTime = str(datetime.datetime.strptime(startTime, '%I:%M %p')).split()[1]
            endTime = str(datetime.datetime.strptime(endTime, '%I:%M %p')).split()[1]
            for d in days.split():
                f.write(str({"id": str(int(cid)), "title": title, "courseNumber": course, "teacher": prof, "difficulty": str(difficulty), "date": d2date(d), "startTime": startTime, "endTime": endTime}).replace("'", '"') + "\n")
        except:
            for d in days.split():
                f.write(str({"id": str(int(cid)), "title": title, "courseNumber": course, "teacher": prof, "difficulty": str(difficulty), "date": d2date(d), "startTime": startTime, "endTime": endTime}).replace("'", '"') + "\n")
f.close()
