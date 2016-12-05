# Author: Abdelrahman M.
import pymysql
import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from account.models import user_type
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout
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
    return TemplateResponse(request, 'administrator/index3.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def create_admin(request):
    """
        Creates and admin for the school. Will not be used by the website. Only once by us to test.
    """
    if request.method == 'GET':
        return TemplateResponse(request, 'administrator/register_admin.html')

    username = request.POST.get("username")
    password = request.POST.get("password")
    school_name = request.POST.get("school_name")
    school_address = request.POST.get("school_address")
    birth_date = request.POST.get("birth_date")
    cur.execute("INSERT INTO Adminstrators(username, e_password, birth_date, school_name, school_address) VALUES(%s,%s,%s,%s,%s)", (username, password, birth_date, school_name, school_address))

    user = User()
    user.username = username
    user.set_password(password)
    user.save()
    type_of_user = user_type()
    type_of_user.user = user
    type_of_user.type = 'administrator'
    type_of_user.save()

    db.commit()

    return HttpResponse('Registered admin successfully')


def view_signed_up_teachers(request):
    username = request.user.get_username()
    #username = "meni"  # HARDCODED AND NEEDS TO BE CHANGED
    cur.execute("SELECT first_name, middle_name, last_name, birth_date, email, gender, e_address, school_name, school_address, years_of_experience FROM Teachers WHERE (school_name, school_address) IN (SELECT school_name, school_address FROM Adminstrators WHERE username=%s) AND username is NULL", (username))


    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['first_name'] = record[0]
        data_dict['middle_name'] = record[1]
        data_dict['last_name'] = record[2]
        data_dict['birth_date'] = record[3]
        data_dict['email'] = record[4]
        data_dict['gender'] = record[5]
        data_dict['e_address'] = record[6]
        data_dict['school_name'] = record[7]
        data_dict['school_address'] = record[8]
        data_dict['years'] = record[9]
        all_data.append(data_dict)

    return TemplateResponse(request, 'administrator/signed_up.html', {"data": all_data})


def approve_teacher(request):
    """
        approves a signedUp teacher
    """
    first_name = request.POST.get("first_name")
    middle_name = request.POST.get("middle_name")
    last_name = request.POST.get("last_name")
    # Set username to the first 2 letters of first name and last name Abdelrahman Meniawy = ab.meniawy
    username = first_name[:2] + '.' + last_name
    password = 'password'

    # Get the chosen applied teacher
    cur.execute("SELECT birth_date, email, gender, e_address, school_name, school_address, years_of_experience FROM Teachers WHERE first_name =%s AND middle_name =%s AND last_name=%s AND username IS NULL", (first_name, middle_name, last_name))
    record = cur.fetchone()

    birth_date = record[0]
    email = record[1]
    gender = record[2]
    address = record[3]
    school_name = record[4]
    school_address = record[5]
    years = record[6]

    # Get type of school (National or International)
    cur.execute("SELECT s_type FROM Schools WHERE name=%s AND s_address=%s", (school_name, school_address))
    type = cur.fetchone()[0]
    salary = 5000
    if type == 'national':
        salary = 3000

    # Add teacher to Teacher with assigned username and password
    cur.execute("UPDATE Teachers SET username =%s, e_password=%s, salary=%s WHERE first_name =%s AND middle_name =%s AND last_name=%s AND username IS NULL", (username, password, salary, first_name, middle_name, last_name))
    # Delete teacher from signedUp as he is now signedUp already

    user = User()
    user.username = username
    user.set_password(password)
    user.save()
    type_of_user = user_type()
    type_of_user.user = user
    type_of_user.type = 'teacher'
    type_of_user.save()

    db.commit()

    return view_signed_up_teachers(request)


def reject_teacher(request):
    """
        reject a certain teacher's application
    """
    first_name = request.POST.get("first_name")
    middle_name = request.POST.get("middle_name")
    last_name = request.POST.get("last_name")

    cur.execute("DELETE FROM signedUpTeachers WHERE first_name =%s AND middle_name=%s AND last_name=%s",
                (first_name, middle_name, last_name))
    db.commit()

    return view_signed_up_teachers(request)


def view_applied_students(request):
    """
        View all signed up students
    """
    username = request.user.get_username()
    #username = "meni"
    cur.execute("SELECT * FROM Child_applied_by_Parent_in_School WHERE (accepted = '0' OR accepted IS NULL) AND (school_name, school_address) IN (SELECT school_name, school_address FROM Adminstrators WHERE username=%s)", (username))

    data = cur.fetchall()

    all_data = []
    for record in data:
        data_dict = {}
        data_dict['parent'] = record[0]
        data_dict['child_ssn'] = record[1]
        data_dict['school_name'] = record[2]
        data_dict['school_address'] = record[3]
        all_data.append(data_dict)

    return TemplateResponse(request, 'administrator/signed_up_students.html', {"data": all_data})


def approve_student(request):
    """
        Approve student's application
    """
    child_ssn = request.POST.get("child_ssn")
    school_name = request.POST.get("school_name")
    school_address = request.POST.get("school_address")

    # Accept child application
    cur.execute("UPDATE Child_applied_by_Parent_in_School SET accepted = b%s WHERE child_ssn = %s AND school_name = %s AND school_address = %s", ("1", child_ssn, school_name, school_address))
    # Create a Student with only the ssn TODO: FAWZY's PART
    # cur.execute("INSERT INTO Students(child_ssn) VALUES(%s)", (child_ssn))

    db.commit()

    return view_applied_students(request)


def reject_student(request):
    """
        Reject student's application
    """
    child_ssn = request.POST.get("child_ssn")
    school_name = request.POST.get("school_name")
    school_address = request.POST.get("school_address")

    # Reject Student's application
    cur.execute("DELETE FROM Child_applied_by_Parent_in_School WHERE child_ssn = %s AND school_name = %s AND school_address = %s", (child_ssn, school_name, school_address))

    db.commit()

    return view_applied_students(request)


def view_accepted_students(request):
    """
        View enrolled students
    """
    username = request.user.get_username()
    #username = "meni"

    cur.execute("SELECT e.student_ssn, e.student_id FROM School_enrolled_Student e INNER JOIN Adminstrators a ON e.school_name = a.school_name AND e.school_address = a.school_address WHERE a.username=%s AND (e.verified = 0 OR e.verified IS NULL) ", (username))

    data = cur.fetchall()

    all_data = []
    for record in data:
        data_dict = {}
        data_dict['child_ssn'] = record[0]
        data_dict['child_id'] = record[1]
        all_data.append(data_dict)

    return TemplateResponse(request, 'administrator/view_accepted_students.html', {"data": all_data})


def verify_student(request):
    """
        Verify student and set username and password to them.
    """
    #username = "meni"
    username = request.user.get_username()
    cur.execute("SELECT school_name, school_address FROM Adminstrators WHERE username=%s", (username))
    data = cur.fetchone()
    school_name = data[0]
    school_address = data[1]
    child_ssn = request.POST.get("child_ssn")
    cur.execute("SELECT name FROM Children WHERE ssn=%s" ,(child_ssn))
    child_name = cur.fetchone()[0]
    child_name = child_name.split()

    try:
        username = child_name[0][:2] + '.' + child_name[1]
    except:
        username = child_name[0]
    password = 'password'

    cur.execute("SELECT id FROM Students WHERE child_ssn=%s", (child_ssn))
    student_id = cur.fetchone()[0]

    cur.execute("UPDATE Students SET username = %s, password_ = %s WHERE child_ssn = %s", (username, password, child_ssn))

    cur.execute("CALL verifyEnrolledStudent(%s,%s,%s,%s)",
                (child_ssn, school_name, school_address, student_id))

    db.commit()
    user = User()
    user.username = username
    user.set_password(password)
    user.save()
    type_of_user = user_type()
    type_of_user.user = user
    type_of_user.type = 'student'
    type_of_user.save()

    return view_accepted_students(request)


def view_school_info(request):
    """
    TODO: NOT FINISHED STILL NEED TO GET USERNAME OF LOGGED IN ADMIN
    Show the school info of the admin
    """
    username = request.user.get_username()
    #username = "meni" # HARDCODED AND NEEDS TO BE CHANGED

    cur.execute("SELECT * FROM Schools WHERE (name, s_address) IN (SELECT school_name, school_address FROM Adminstrators a WHERE a.username =%s)", (username))
    data = cur.fetchone()
    school = {}

    school['school_name'] = data[0]
    school['school_address'] = data[1]
    school['phone_number'] = data[2]
    school['email'] = data[3]
    school['information'] = data[4]
    school['vision'] = data[5]
    school['mission'] = data[6]
    school['language'] = data[7]
    school['fees'] = data[8]
    school['type'] = data[9]

    return TemplateResponse(request, 'administrator/edit_school.html', {"data": school})


def edit_school_info(request):
    """
        Take school info from request and update record
    """

    original_name = request.POST.get("original_school_name")
    original_address = request.POST.get("original_school_address")

    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    information = request.POST.get("information")
    vision = request.POST.get("vision")
    mission = request.POST.get("mission")
    language = request.POST.get("language")
    fees = request.POST.get("fees")
    type = request.POST.get("type")

    cur.execute("UPDATE Schools SET phone_number =%s, email = %s, information =%s, vision =%s, mission =%s, main_language =%s, fees =%s, s_type =%s WHERE name=%s AND s_address =%s",(phone_number, email, information, vision, mission, language, fees, type, original_name, original_address))

    db.commit()

    return view_school_info(request)


def post_announcement(request):
    """
        Shows post announcement form or saves it.
    """
    if request.method == 'GET':
        return TemplateResponse(request, 'administrator/post_announcement.html')

    username = request.user.get_username()
    #username = "meni"  # HARDCODED AND NEEDS TO BE CHANGED

    # Now get the admin's id number
    cur.execute("SELECT id FROM Adminstrators WHERE username=%s", (username))
    id_ = cur.fetchone()[0]
    # Fetch remaining attributes
    title = request.POST.get("title")
    description = request.POST.get("description")
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    type = request.POST.get("type")

    cur.execute("INSERT INTO Announcements(title, description_, an_date, type_, admin_id) VALUES(%s,%s,%s,%s,%s)",(title, description, date, type, id_))
    db.commit()

    return index(request)


def create_activity(request):
    """
        Show creation page or create activity with passed attributes.
    """
    username = request.user.get_username()
    #username = "meni"  # HARDCODED AND NEEDS TO BE CHANGED

    if request.method == 'GET':
        cur.execute("SELECT school_name, school_address FROM Adminstrators WHERE username=%s", (username))
        school = cur.fetchone()
        school_name = school[0]
        school_address = school[1]
        cur.execute("SELECT username, id FROM Teachers WHERE school_name=%s AND school_address=%s", (school_name, school_address))
        teachers_data = cur.fetchall()
        all_teachers = []
        for teacher in teachers_data:
            teacher_dict = {}
            teacher_dict['username'] = teacher[0]
            teacher_dict['id'] = teacher[1]
            all_teachers.append(teacher_dict)

        return TemplateResponse(request, 'administrator/create_activity.html', {"data": all_teachers})

    date = request.POST.get("date")
    location = request.POST.get("location")
    type = request.POST.get("type")
    equipment = request.POST.get("equipment")
    description = request.POST.get("description")
    teacher_id = request.POST.get("id")

    cur.execute("INSERT INTO Activities(ac_date, location, ac_type, equipment, ac_description, teacher_id) VALUES(%s,%s,%s,%s,%s,%s)", (date, location, type, equipment, description, teacher_id))
    db.commit()

    return index(request)


def assign_teacher_to_course(request):
    """
        Show assigning page for teacher to course. Or create the relation
    """
    username = request.user.get_username()
    #username = "meni"

    if request.method == 'GET':
        cur.execute("SELECT school_name, school_address FROM Adminstrators WHERE username=%s", (username))
        school = cur.fetchone()
        school_name = school[0]
        school_address = school[1]
        cur.execute("SELECT username, id FROM Teachers WHERE school_name=%s AND school_address=%s", (school_name, school_address))
        teachers_data = cur.fetchall()
        all_teachers = []
        for teacher in teachers_data:
            teacher_dict = {}
            teacher_dict['username'] = teacher[0]
            teacher_dict['id'] = teacher[1]
            all_teachers.append(teacher_dict)

        cur.execute("SELECT code FROM Courses")
        courses = cur.fetchall()
        all_courses = []
        for course in courses:
            all_courses.append(course[0])

        return TemplateResponse(request, 'administrator/assign_teacher_to_course.html', {"data": all_teachers, "courses": all_courses})

    course_code = request.POST.get("course_code")
    teacher_id = request.POST.get("teacher_id")

    cur.execute("INSERT INTO Course_Teached_By_Teacher(course_code, teacher_id) VALUES(%s,%s)", (course_code, teacher_id))

    db.commit()

    return index(request)

