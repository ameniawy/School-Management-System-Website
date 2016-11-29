# Author : Mohab
"""
    Teacher URLS FILE
"""
from django.conf.urls import url
from django.conf.urls import include
import teacher.views


urlpatterns = [


    url(r'^courses/', teacher.views.view_courses, name='view_courses'),
    url(r'^post_assignment/', teacher.views.post_assignment, name='post_assignment'),
    url(r'^posted_assignment/', teacher.views.posted_assignment, name='posted_assignment'),
    url(r'^view_assignments/', teacher.views.view_assignments, name='view_assignment'),
    url(r'^write_report/', teacher.views.write_report, name='write_report'),
    url(r'^submitted_report/', teacher.views.submitted_report, name='submitted_report'),
    url(r'^questions/', teacher.views.question_for_course, name='question_for_course'),
    url(r'^view_questions/', teacher.views.view_questions, name='view_questions'),
    url(r'^view_students/', teacher.views.view_students, name='view_students'),
    # Teacher Home
    url(r'^$', teacher.views.index, name='teacher_index')



]
