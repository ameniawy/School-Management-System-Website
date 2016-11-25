
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
import pymysql



db =  pymysql.connect(host='localhost', # your host, usually localhost
			 user='root', # your username
			  passwd='root', # your password
			  db='school_system') # name of the data base
db.set_charset('utf8mb4')
# you must create a Cursor object. It will let
#  you execute all the queries you need
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

	
	
	return TemplateResponse(request,'main/main.html',{"data": all_data})


def home(request):
	html = '<h1>Hi everyone this is our first page</h1>'
	return HttpResponse(html)
