# Author : Abdelraman M.
"""
    Account URLS FILE
"""
from django.conf.urls import url
from django.conf.urls import include
from . import views

app_name = 'account'
urlpatterns = [

    url(r'^register_parent/', views.register_parent, name='register_parent'),
    url(r'^register_teacher/', views.register_teacher, name='register_teacher'),
    url(r'^view_schools/', views.view_schools, name='view_schools'),
    url(r'^view_school_info/', views.view_school_info, name='view_school_info'),
    url(r'^search/', views.search, name='search'),
    url(r'^login/', views.login_view, name='login_view'),

    url(r'^$', views.index, name='index'),

]