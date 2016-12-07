"""AuthenticationApp URL Configuration

Created by Naman Patwari on 10/4/2016.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login$', views.auth_login, name='Login'),
    url(r'^logout$', views.auth_logout, name='Logout'),
    url(r'^register-teacher$', views.auth_register_teacher, name='RegisterTeacher'),
	url(r'^register-engineer$', views.auth_register_engineer, name='RegisterEngineer'),
	url(r'^register-student$', view.auth_register_engineer, name='RegisterStudent'),
    url(r'^update$', views.update_profile, name='UpdateProfile'),    
]
