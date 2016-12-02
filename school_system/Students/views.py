from django.shortcuts import render

# Create your views here.
import pymysql

from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
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
    return
def view_student_info(request):
    return

def update_student_info(request):
    return

def view_student_courses(request):
    return
def post_question_per_course(request):
    return
def view_all_questions_course(request):
    return
def view_assignments_course(request):
    return
def submit_assignment_course(request):
	return
def view_activities(request):
    return
def join_activities(request):
     return
def view_grades_assignment_course(request):
     return
def view_clubs(request):
     return
def join_clubs(request):
    return


