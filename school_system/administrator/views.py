from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
import pymysql
from django.conf import settings

db = pymysql.connect(host=settings.DB_HOST,  # your host, usually localhost
                     user=settings.DB_USERNAME,  # your username
                     passwd=settings.DB_PASSWORD,  # your password
                     db=settings.DB_NAME)  # name of the data base
db.set_charset('utf8mb4')
# you must create a Cursor object. It.DB_HOST  you execute all the queries you need
cur = db.cursor()


# Create your views here.
def school_home(request):
    cur.execute("SELECT name, s_address, s_type FROM Schools")
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['name'] = record[0]
        data_dict['address'] = record[1]
        all_data.append(data_dict)

    return TemplateResponse(request, 'main/main.html', {"data": all_data})




def view_signedUp_teachers(request):
    cur.execute("SELECT * FROM signedUpTeachers")
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
    first_name = request.POST.get("first_name")
    middle_name = request.POST.get("middle_name")
    last_name = request.POST.get("last_name")
    username = first_name[:2] + '.' + last_name
    password = 'password'

    cur.execute("SELECT * FROM signedUpTeachers WHERE first_name =%s AND middle_name =%s AND last_name=%s", (first_name, middle_name, last_name))
    record = cur.fetchone()
    birth_date = record[3]
    email = record[4]
    gender = record[5]
    address = record[6]
    school_name = record[7]
    school_address = record[8]
    years = record[9]
    cur.execute("INSERT INTO Teachers(username, e_password, first_name, middle_name, last_name, birth_date, email, gender, e_address, school_name, school_address, years_of_experience) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(username, password, first_name, middle_name, last_name, birth_date, email, gender, address, school_name, school_address, years))
    data = [record]

    db.commit()


    return TemplateResponse(request, 'main/main.html', {"data": data})
