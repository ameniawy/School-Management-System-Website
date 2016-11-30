from django.shortcuts import render
from django.http import HttpResponse
import pymysql
from django.conf import settings
import datetime
# Create your views here.


db =  pymysql.connect(host=settings.DB_HOST, user=settings.DB_USERNAME,passwd=settings.DB_PASSWORD,db=settings.DB_NAME)
db.set_charset('utf8mb4')
# you must create a Cursor object. It.DB_HOST  you execute all the queries you need
cur = db.cursor()




def  home(request):
    unkown_user = 'mhmd'
    cur.execute("SELECT name, s_address, s_type FROM Schools")
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['name'] = record[0]
        data_dict['address'] = record[1]
        all_data.append(data_dict)

    return render(request,'parent/apply/apply_school.html',{'schools':all_data,'user':unkown_user})


def apply_child(request):
    unkown_user = 'mhmd'
    if request.method=='POST':
        ssn = request.POST.get('ssn')
        name = request.POST.get('name')
        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        school_address = request.POST.get('address')
        school_name = request.POST.get('school_name')
        cur.execute('call createChild(%s,%s,%s,%s,%s)',(unkown_user, ssn, name , birth, gender))
        cur.execute('call applyForChildInSchool(%s,%s,%s,%s)', (unkown_user, ssn, school_name, school_address))
        db.commit()
        return HttpResponse('done')
    return HttpResponse('Failed')


def accepted_children(request):
    unkown_user = 'mhmd'
    exec2= "select cap.school_name, cap.school_address, cap.child_ssn from Child_applied_by_Parent_in_School cap where cap.accepted = 1 and cap.child_ssn in (select ssn from Children where parent_username = %s) order by cap.child_ssn;"
    cur.execute(exec2, (unkown_user))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['name'] = record[0]
        data_dict['address'] = record[1]
        data_dict['child_ssn'] = record[2]

        all_data.append(data_dict)
    print(all_data)

    return render(request,'parent/choose/accpeted_schools.html', {'schools':all_data,'user':unkown_user})

def choose_school(request):
    unkown_user = 'mhmd'
    exec = "update Child_applied_by_Parent_in_School set choosen = 1 where parent_username = %s and child_ssn = %s and school_name = %s and school_address= %s"
    exec2 = "select * from  Child_applied_by_Parent_in_School where parent_username = %s and child_ssn = %s  and choosen = 1"
    exec3 = "insert into students(child_ssn) values (%s);"
    exec4 = 'select id from students where child_ssn= %s'
    exec5 = 'insert into School_enrolled_Student(student_id, student_ssn, school_name, school_address) values(%s,%s,%s,%s)'
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        school_address = request.POST.get('school_address')
        ssn = request.POST.get('ssn')
        cur.execute(exec2,(unkown_user,ssn))
        data = cur.fetchall()
        all_data = []
        for record in data:
            data_dict = {}
            data_dict['name'] = record[0]
            data_dict['address'] = record[1]
            all_data.append(data_dict)
        print(data)
        if len(all_data)>0:
            return HttpResponse('You already applied for this child')
        print('hi')
        cur.execute(exec,(unkown_user,ssn,school_name,school_address))
        db.commit()

        cur.execute(exec4,(ssn))
        student_id = cur.fetchall()[0][0]
        print(student_id)
        cur.execute(exec5,(student_id,ssn, school_name,school_address))
        db.commit()
        return HttpResponse('done')
    return render(request, 'parent/form.html', {})


def reports(request):
    unkown_user = 'mhmd'
    cur.execute('call parentViewChildrenReports(%s)', (unkown_user))
    data = cur.fetchall()
    all_data = []
    exec = 'select first_name , last_name from teachers where id = %s'
    for record in data:
        data_dict = {}
        data_dict['date'] = record[0]
        data_dict['student_id'] = record[1]
        data_dict['teacher_id'] = record[2]
        d = str(data_dict['date'])+''
        data_dict['format_date'] = d

        cur.execute(exec,record[2])
        teacher_name = cur.fetchall()[0][0]
        data_dict['teacher_name'] = teacher_name
        data_dict['content'] = record[3]
        all_data.append(data_dict)

    return render(request, 'parent/reports/reports.html', {'reports':all_data,'user':unkown_user})


def report_reply(request):
    unkown_user = 'mhmd'
    if request.method == 'POST':
        parent_username = unkown_user
        report_date = request.POST.get('report_date')
        student_id = request.POST.get('student_id')
        teacher_id = request.POST.get('teacher_id')
        reply = request.POST.get('reply')
        cur.execute('call parentReplyonChildReport(%s,%s,%s,%s,%s)', (parent_username,report_date,student_id,teacher_id,reply))
        db.commit()
        return HttpResponse("done")

    return render(request, 'parent/form.html', {})



def teachers(request):
    unkown_user = 'mhmd'
    cur.execute('call viewTeachersofMyChildren(%s)', (unkown_user))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['name'] = record[3]
        data_dict['id'] = record[0]
        cur.execute('call parentViewOverallTeacherRating(%s)', (record[0]))
        data2 = cur.fetchall()
        if len(data2)>0:
            data_dict['rating'] = data2[0][2]
        all_data.append(data_dict)
    return render(request, 'parent/teachers/teachers.html', {'teachers':all_data,'user':unkown_user})



def rate_teacher(request):
    unkown_user = 'mhmd'

    if request.method=="POST":
        parent_username = unkown_user
        teacher_id = request.POST.get('teacher_id')
        rating = request.POST.get('rating')
        cur.execute('call parentRatesTeacher(%s,%s,%s)',(parent_username,teacher_id,rating))
        db.commit()
        return HttpResponse("Done")

    return HttpResponse("error")


def schools(request):
    unkown_user = 'mhmd'
    cur.execute('call parentViewSchoolsofChildren(%s)',(unkown_user))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['name'] = record[0]
        data_dict['address'] = record[1]
        all_data.append(data_dict)
    return render(request, 'parent/accepted_schools/my_school.html', {'schools':all_data,'user':unkown_user})

def write_review(request):
    unkown_user = 'mhmd'

    if request.method == 'POST':
        parent_user = unkown_user
        school_name = request.POST.get('school_name')
        school_address = request.POST.get('school_address')
        review = request.POST.get('review')
        cur.execute('call writeSchoolReview(%s,%s,%s,%s)',(parent_user,school_name,school_address,review))
        db.commit()
        return HttpResponse('done')
    return render(request, 'parent/form.html', {})



def get_reviews(request):
    unkown_user = 'mhmd'

    cur.execute('select * from SchoolReviews where parent_username = %s',(unkown_user))
    data = cur.fetchall()
    all_data = []
    for record in data:
        data_dict = {}
        data_dict['parent_username'] = record[0]
        data_dict['school_name'] = record[1]
        data_dict['school_address'] = record[2]
        data_dict['review'] = record[3]
        all_data.append(data_dict)
    return render(request, 'parent/reviews/reviews.html', {'reviews':all_data,'user':unkown_user})


def delete_review(request):
    unkown_user = 'mhmd'

    if request.method == 'POST':
        parent_user = unkown_user
        school_name = request.POST.get('school_name')
        school_address = request.POST.get('school_address')
        print(school_name)
        print(school_address)

        cur.execute('call deleteSchoolReview(%s,%s,%s)',(parent_user,school_name,school_address))
        db.commit()
        return HttpResponse('done deleted')
    return render(request, 'parent/form.html', {})



























