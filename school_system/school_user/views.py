from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
import pymysql
from django.conf import settings

# Create your views here.
db =  pymysql.connect(host=settings.DB_HOST, # your host, usually localhost
			 user=settings.DB_USERNAME, # your username
			  passwd=settings.DB_PASSWORD, # your password
			  db=settings.DB_NAME) # name of the data base
db.set_charset('utf8mb4')
# you must create a Cursor object. It.DB_HOST  you execute all the queries you need
cur = db.cursor()


# this is an incomplete version of the registeration of a user
def register(request):
	username = request.GET['username']
	password = request.GET['password']
	user_type = request.GET['user_type']


# function to return all types of schools categorized by their type
def view_schools(request):
	cur.execute("SELECT name, address FROM School_offers_Level WHERE l_type =%s;",('elementary'))
	elementary = cur.fetchall()
	all_elementary = []
	for school in elementary:
		school_dict = {}
		school_dict['name'] = school[0]
		school_dict['address'] = school[1]
		all_elementary.append(school_dict)

	cur.execute("SELECT name, address FROM School_offers_Level WHERE l_type =%s;",('middle'))
	middle = cur.fetchall()
	all_middle = []
	for school in middle:
		school_dict = {}
		school_dict['name'] = school[0]
		school_dict['address'] = school[1]
		all_middle.append(school_dict)

	cur.execute("SELECT name, address FROM School_offers_Level WHERE l_type =%s;",('high'))
	high = cur.fetchall()
	all_high = []
	for school in elementary:
		school_dict = {}
		school_dict['name'] = school[0]
		school_dict['address'] = school[1]
		all_high.append(school_dict)


	return TemplateResponse(request,'main/main.html',{"elementary_schools": all_elementary, "high_schools": all_high, "middle_schools":all_middle})




