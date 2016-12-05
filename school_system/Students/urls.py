from django.conf.urls import url
from .views import *
import Students.views


app_name='Students'

urlpatterns = [
#profile displaying info about the student and updating info
    url(r'^student_info/$',Students.views.view_student_info, name='Students_info'),
    url(r'^updating_info/$',Students.views.update_student_info, name='Students_updating_info'),


   url(r'^courses/$', Students.views.view_student_courses, name='student_courses'),

#He/she can then choose a course to post a question about it, where a teacher would later answer.    
 url(r'^post_question_course/$', Students.views.post_question_per_course, name='student_questions_course'),
     #url(r'^question_course_answer/$', Students.views., name='teacher_questions_answers'),

#View all questions asked on a certain course along with their answers.
    url(r'^view_allquestion_course/$', Students.views.view_all_questions_course, name='view_question_per_course'),

#  He/she can then choose a course to view assignments posted about it and submit a solution for it.
    url(r'^view_assignment_course/$', Students.views.view_assignments_course, name='student_view_assignment_course'),
    url(r'^submit_assignment_course/$', Students.views.submit_assignment_course, name='student_submit_assignment_course'),
#   View a list of activities offered by the school (all the information about the activity and the teacher supervising it). The student can then join any activity on the condition that not to join two activities of the same type on the same date.   
    url(r'^activities/$', Students.views.view_activities, name='student_get_activities'),
    url(r'^join_activities/$', Students.views.join_activities, name='student_join_activities'),

#   View the grade of the assignments he/she solved per course.
    url(r'^grades_assignment_course/$', Students.views.view_grades_assignment_course, name='student_grades_assignment'),
 
 # For high school students only: A student can view a list of clubs in his/her school and join any of them.
    url(r'^clubs/$', Students.views.view_clubs, name='student_clubs'),
    url(r'^clubs_join/$', Students.views.join_clubs, name='student_join_clubs'),



url(r'^$', Students.views.index, name='student_index'),



]