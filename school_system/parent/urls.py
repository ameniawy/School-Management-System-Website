from django.conf.urls import url
from .views import *
app_name='parent'
urlpatterns = [
    url(r'^home/$',home, name='parent_home'),
    url(r'^accepted/$', accepted_children, name='parent_accepted'),
    url(r'^apply/$', apply_child, name='parent_apply'),
    url(r'^choose/$', choose_school, name='parent_choose'),
    url(r'^reports/$', reports, name='parent_reports'),
    url(r'^report_reply/$', report_reply, name='parent_reply'),
    url(r'^teachers/$', teachers, name='parent_teachers'),
    url(r'^teachers_rate/$', rate_teacher, name='parent_rate'),
    url(r'^schools/$', schools, name='schools'),
    url(r'^write_review/$', write_review, name='parent_write'),
url(r'^reviews/$', get_reviews, name='reviews')

]