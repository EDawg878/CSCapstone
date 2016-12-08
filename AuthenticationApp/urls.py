"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register$', views.auth_register, name='Register'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),
    url(r'^update_engineer$', views.update_engineer_profile, name='UpdateEngineer'),
    url(r'^update_teacher$', views.update_teacher_profile, name='UpdateTeacher'),
    url(r'^update_student$', views.update_student_profile, name='UpdateStudent'),
	
	url(r'^register_engineer$', views.register_engineer, name='RegisterEngineer'), 
	url(r'^register_teacher$', views.register_teacher, name='RegisterTeacher'),
	url(r'^register_student$', views.register_student, name='RegisterStudent')
]
