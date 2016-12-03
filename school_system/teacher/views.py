#Author: Mohab
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
# Create your views here.


def index(request):
    return TemplateResponse(request, 'teacher/index3.html')

# 1 View a list of courses names taught by him/her, listed based on their level then their grade.


def view_courses(request):
    teacher_id = 3
    #cur.execute("SELECT * FROM Schools WHERE (name, s_address) IN (SELECT school_name, school_address FROM Adminstrators a WHERE a.username =%s)", (username))
    cur.execute("SELECT * FROM Courses c where c.code in (select ct.course_code from Course_Teached_By_Teacher ct where ct.teacher_id = %s) order by c.c_level, c.grade_code", (teacher_id))
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

    return TemplateResponse(request, 'teacher/courses.html', {"data": all_data})


# 2 Post assignments for any course taught by him/her. Every assignment is assigned to one course and
# has a due date and content.

def post_assignment(request):
    return TemplateResponse(request, 'teacher/post_assignment.html', {"data": 'not posted yet'})


def posted_assignment(request):
    teacher_id = 3
    code =  request.GET.get('course_code')
    ddate =  request.GET.get('due_date')
    pdate =  request.GET.get('post_date')
    content =  request.GET.get('content')
    num =  request.GET.get('ass_num')
    cur.execute("INSERT INTO Assignments(a_number, course_code, content, due_date, post_dat, teacher_id) VALUES(%s, %s, %s, %s, %s, %s)", (num, code, content, ddate, pdate, teacher_id))
    db.commit()
    data = 'posted!'
    # how to notify him??
    return TemplateResponse(request, 'teacher/post_assignment.html', {"data": data})


def view_assignments(request):
    teacher_id = 3
    cur.execute("SELECT * FROM Assignments a where a.teacher_id = %s", (teacher_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['ass_num'] = record[0]
        data_dict['course_code'] = record[1]
        data_dict['content'] = record[2]
        data_dict['due_date'] = record[3]
        data_dict['post_date'] = record[4]
        all_data.append(data_dict)

    return TemplateResponse(request, 'teacher/assignments.html', {"data": all_data})


def view_solutions(request):
    """
        View solutions of an assignment belonging to a course.
    """
    course_code = request.POST.get('course_code')
    ass_num = request.POST.get('ass_num')
    cur.execute("SELECT * FROM Assignment_solved_by_Student WHERE course_code=%s AND ass_number=%s", (course_code, ass_num))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['ass_num'] = record[0]
        data_dict['course_code'] = record[1]
        data_dict['student_id'] = record[2]
        data_dict['answer'] = record[3]
        all_data.append(data_dict)

    return TemplateResponse(request, 'teacher/view_solutions.html', {"data": all_data})


def grade_assignment(request):
    """
        Update assignment solution with given grade.
    """
    course_code = request.POST.get('course_code')
    ass_num = request.POST.get('ass_num')
    student_id = request.POST.get('student_id')
    grade = request.POST.get('ass_grade')

    cur.execute("UPDATE Assignment_solved_by_Student SET grade=%s WHERE ass_number=%s AND course_code=%s AND student_id=%s", (grade, ass_num, course_code, student_id))

    return view_assignments(request)




# 4 Write a report about a student in a specific course. The report contains his/her comments.
# but the course part wasn't mentioned before!!!


def write_report(request):
    return TemplateResponse(request, 'teacher/write_report.html', {})


def submitted_report(request):
    student_id = request.GET.get('student_id')
    date = request.GET.get('date')
    content = request.GET.get('content')
    teacher_id = 3
    cur.execute("INSERT INTO Reports(report_date, student_id, teacher_id, content) VALUES(%s, %s, %s, %s)", (date, student_id, teacher_id, content))
    db.commit()
    return TemplateResponse(request, 'teacher/write_report.html', {"date": date, "student_id": student_id, "teacher_id": teacher_id, "content": content})


# 5 View a list of questions for a certain course along with the name of the student who asked it, and
# provide an answer to them one by one.
# how to answer???
def question_for_course(request):
    return TemplateResponse(request, 'teacher/questions.html', {})


def view_questions(request):
    code = request.GET.get('course_code')
    teacher_id = 3
    cur.execute("SELECT * from Questions q where q.course_code=%s", (code))
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

    return TemplateResponse(request, 'teacher/questions.html', {"data": all_data})


def post_answer(request):
    code = request.GET.get('course_code')
    q_number = request.GET.get('q_number')
    answer = request.GET.get('answer')
    cur.execute("UPDATE Questions set answer=%s where course_code=%s and q_number", (answer, code, q_number))
    return TemplateResponse(request, 'teacher/questions.html', {})

# 6 View a list of students that a teacher teaches categorized by their grades and ordered by their names
# (first name and last name).


def view_students(request):
    teacher_id = 3
    cur.execute("SELECT ss.id, ss.username from Students ss, School_enrolled_Student ses where ses.student_id = ss.id and ss.id in (select s.student_id from School_enrolled_Student s where s.grade_code in (select distinct grade_code from Courses where code in (select distinct course_code from Course_Teached_By_Teacher where teacher_id = %s))) order by ses.grade_code, ss.username", (teacher_id))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['id'] = record[0]
        data_dict['username'] = record[1]
        all_data.append(data_dict)

    return TemplateResponse(request, 'teacher/my_students.html', {"data": all_data})
