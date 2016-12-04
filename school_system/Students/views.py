from django.shortcuts import render

# Create your views here.
import pymysql
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
    return   TemplateResponse(request, 'Students/index.html')
def view_student_info(request):
    username = "honda"
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()
    cur.exexute("SELECT * FROM Students s inner join children c on s.ssn=c.ssn where s.id=%s ",(student_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['id'] = record[0]
        data_dict['course_code'] = record[1]
        data_dict['student_id'] = record[2]
        data_dict['q_date'] = record[3]
        data_dict['question'] = record[4]
        data_dict['answer'] = record[5]
        all_data.append(data_dict)
       

    
     

    
    
     


    return 
    

def update_student_info(request):
    return

def view_student_courses(request):
    username = "honda"
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()
    cur.execute("CALL viewAllCoursesItake(%s)",(student_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['code'] = record[0]
        data_dict['name'] = record[1]
        data_dict['c_level'] = record[2]
        data_dict['description_'] = record[3]
        data_dict['grade_code'] = record[4]
        
        all_data.append(data_dict)
       

    
     

    
    
     


    return TemplateResponse(request, 'Students/courses.html', {"data": all_data})
    
def post_question_per_course(request):
    return
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
   
    #code = "CSEN202"
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
	return
def view_activities(request):
    
    username = "honda"
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()
    cur.execute("CALL studentViewactivites(%s)",(student_id))
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
     return
def view_grades_assignment_course(request):

     return
def view_clubs(request):
    username = "honda"
    cur.execute("SELECT id FROM Students WHERE username=%s", (username))
    student_id = cur.fetchone()
    cur.execute("CALL viewClubsInMySchool(%s)",(student_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['club_name'] = record[0]
        
        
        all_data.append(data_dict)
       

    
     

    
    
     


    return TemplateResponse(request, 'Students/clubs.html', {"data": all_data})
    

    
def join_clubs(request):
    return


