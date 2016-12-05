# Author : Abdelraman M.
"""
    ADMINISTRATOR URLS FILE
"""
from django.conf.urls import url
from django.conf.urls import include
import administrator.views


urlpatterns = [



    url(r'^signed_up/', administrator.views.view_signed_up_teachers, name='view_signedUp_teachers'),
    # Accept or reject teachers' applications
    url(r'^approve/', administrator.views.approve_teacher, name='approve_teacher'),
    url(r'^reject/', administrator.views.reject_teacher, name='reject_teacher'),

    # Accept or reject students' applications
    url(r'^signed_up_students/', administrator.views.view_applied_students, name='view_applied_students'),
    url(r'^approve_student/', administrator.views.approve_student, name='approve_student'),
    url(r'^reject_student/', administrator.views.reject_student, name='reject_student'),

    url(r'^view_accepted_students/', administrator.views.view_accepted_students, name='view_accepted_students'),
    url(r'^verify_student/', administrator.views.verify_student, name='verify_student'),

    url(r'^view_school_info/', administrator.views.view_school_info, name='view_school_info'),
    url(r'^edit_school_info/', administrator.views.edit_school_info, name='edit_school_info'),

    url(r'^post_announcement/', administrator.views.post_announcement, name='post_announcement'),

    url(r'^create_activity/', administrator.views.create_activity, name='create_activity'),

    url(r'^assign_teacher_to_course/', administrator.views.assign_teacher_to_course, name='assign_teacher_to_course'),

    url(r'^logout/', administrator.views.logout_user, name='logout_user'),


    url(r'^register_admin/', administrator.views.create_admin, name='create_admin'),



    # Admin Home
    url(r'^$', administrator.views.view_signed_up_teachers, name='admin_index'),



]