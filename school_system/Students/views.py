from django.shortcuts import render

# Create your views here.
import pymysql
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required


db = pymysql.connect(host=settings.DB_HOST,  # your host, usually localhost
                     user=settings.DB_USERNAME,  # your username
                     passwd=settings.DB_PASSWORD,  # your password
                     db=settings.DB_NAME)  # name of the data base
db.set_charset('utf8mb4')
# you must create a Cursor object. It.DB_HOST  you execute all the queries you need
cur = db.cursor()


def index(request):
    return TemplateResponse(request, 'Students/index.html')


def view_student_info(request):
    #username = "honda"
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]
    cur.execute("SELECT c.ssn, c.name, c.birth_date, c.gender, c.age, c.parent_username, s.username FROM Students s inner join Children c on s.child_ssn=c.ssn where s.id=%s ",(student_id))
    record = cur.fetchone()

    data_dict = {}
    data_dict['ssn'] = record[0]
    data_dict['name'] = record[1]
    data_dict['birth_date'] = record[2]
    data_dict['gender'] = record[3]
    data_dict['age'] = record[4]
    data_dict['parent_username'] = record[5]
    data_dict['username'] = record[5]

    return TemplateResponse(request, 'Students/student_info.html', {"data": data_dict})
    

def update_student_info(request):
    return


def view_student_courses(request):
    #username = "honda"
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]
    cur.execute("CALL viewAllCoursesItake(%s)", (student_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['code'] = record[0]
        data_dict['name'] = record[1]
        data_dict['c_level'] = record[2]
        data_dict['description'] = record[3]
        data_dict['grade_code'] = record[4]
        
        all_data.append(data_dict)

    return TemplateResponse(request, 'Students/courses.html', {"data": all_data, "student_id": student_id})


def post_question_per_course(request):

    course_code = request.POST.get("course_code")
    student_id = request.POST.get("student_id")
    question = request.POST.get("question")
    date = datetime.datetime.today().strftime('%Y-%m-%d')

    cur.execute("INSERT INTO Questions(course_code, student_id, q_date, question) VALUES(%s,%s,%s,%s)", (course_code, student_id, date, question))
    db.commit()

    return view_student_courses(request)


def view_all_questions_course(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'Students/questions_form.html')

    code = request.POST.get('course_code')
    #code = "CSEN202"
    cur.execute("SELECT * from Questions where course_code=%s ", (code))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['q_number'] = record[0]
        data_dict['course_code'] = record[1]
        data_dict['student_id'] = record[2]
        data_dict['q_date'] = record[3]
        data_dict['question'] = record[4]
        data_dict['answer'] = record[5]
        all_data.append(data_dict)

    return TemplateResponse(request, 'Students/questions.html', {"data": all_data})


def view_assignments_course(request):
    if request.method == 'GET':
        return TemplateResponse(request, 'Students/assignment_form.html')

    code = request.POST.get('course_code')

    cur.execute("SELECT * from Assignments where course_code=%s ", (code))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['a_number'] = record[0]
        data_dict['course_code'] = record[1]
        data_dict['content'] = record[2]
        data_dict['due_date'] = record[3]
        data_dict['post_dat'] = record[4]
        data_dict['teacher_id'] = record[5]
        all_data.append(data_dict)

    return TemplateResponse(request, 'Students/assignments.html', {"data": all_data})


def submit_assignment_course(request):

    if request.method == 'GET':
        return TemplateResponse(request, 'Students/assignmentsubmission_form.html')

    #username = "honda"
    username = request.user.get_username()
    exec1 = "insert into Assignment_solved_by_Student(ass_number, course_code,student_id, answer) values(%s, %s, %s, %s);"
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]

    ass_number = request.POST.get('ass_number')
    code = request.POST.get('course_code')
    answer = request.POST.get('answer')
    cur.execute(exec1, (ass_number, code, student_id, answer))
    db.commit()

    return HttpResponse('done')


def view_activities(request):
    
    #username = "honda"
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]

    sql = "select * from Activities where teacher_id in(select t.id from Teachers t where (t.school_name, t.school_address) IN (SELECT school_name, school_address FROM School_enrolled_Student WHERE student_id =%s));"
    #cur.execute("CALL studentViewactivites2(%s)", (student_id))
    cur.execute(sql, (student_id))

    data = cur.fetchall()


    all_data = []
    for record in data:
        data_dict = {}
        data_dict['ac_date'] = record[0]
        data_dict['location'] = record[1]
        data_dict['ac_type'] = record[2]
        data_dict['equipment'] = record[3]
        data_dict['ac_description'] = record[4]
        data_dict['teacher_id'] = record[5]
        all_data.append(data_dict)

    return TemplateResponse(request, 'Students/activities.html', {"data": all_data})


def join_activities(request):

    #username = "honda"
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]
    cur.execute("SELECT a.ac_date, a.ac_type FROM Activities a INNER JOIN Activity_joined_by_Student aj ON (aj.activity_date = a.ac_date AND aj.activity_location = a.location) WHERE aj.student_id=%s", (student_id))
    ac = cur.fetchone()
    activity_date = request.POST.get('activity_date')
    activity_type = request.POST.get('activity_type')
    activity_location = request.POST.get('activity_location')
    print "okkk"
    print ac

    if ac is not None and activity_type == ac[1] and activity_date == ac[0]:
        return HttpResponse("<h1>Cannot join activity, you have an activity with the same type and date</h1>")

    cur.execute("INSERT INTO Activity_joined_by_Student(student_id, activity_date, activity_location) VALUES(%s,%s,%s)", (student_id, activity_date, activity_location))
    db.commit()

    return view_activities(request)


def view_grades_assignment_course(request):

    if request.method == 'GET':
        return TemplateResponse(request, 'Students/assignmentgraded_form.html')

    #username = "honda"
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]
    code = request.POST.get('course_code')

    cur.execute("CALL ViewGradedAssignments(%s,%s)", (student_id, code))
    data = cur.fetchall()

    all_data = []
    for record in data:
        data_dict = {}
        data_dict['ass_number'] = record[0]
        data_dict['course_code'] = record[1]
        data_dict['student_id'] = record[2]
        data_dict['answer'] = record[3]
        data_dict['grade'] = record[4]
        
        all_data.append(data_dict)

    return TemplateResponse(request, 'Students/assignmentsgrades.html', {"data": all_data})
    

def view_clubs(request):
    #username = "honda"
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]
    sql = "SELECT * FROM Clubs WHERE (school_name, school_address) IN (SELECT school_name, school_address FROM School_enrolled_Student WHERE student_id=%s)"
    cur.execute(sql, (student_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['club_name'] = record[0]
        data_dict['school_name'] = record[1]
        data_dict['school_address'] = record[2]
        data_dict['purpose'] = record[3]
        all_data.append(data_dict)

    return TemplateResponse(request, 'Students/clubs.html', {"data": all_data})
    

def join_clubs(request):
    username = request.user.get_username()
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()[0]
    club_name = request.POST.get('club_name')
    school_name = request.POST.get("school_name")
    school_address = request.POST.get("school_address")
    cur.execute("INSERT INTO Club_joined_by_Student(student_id, school_name, school_address, club_name) VALUES(%s,%s,%s,%s)", (student_id, school_name, school_address, club_name))
    db.commit()

    return index(request)
