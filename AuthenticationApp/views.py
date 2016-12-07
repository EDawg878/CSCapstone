"""AuthenticationApp Views

Created by Naman Patwari on 10/4/2016.
"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from CompaniesApp.models import Engineer
from UniversitiesApp.models import Teacher
from .forms import LoginForm, RegisterForm, UpdateForm
from CompaniesApp.forms import EngineerForm
from UniversitiesApp.forms import TeacherForm 
from .models import MyUser, Student

# Auth Views

def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if next_url is None:
		next_url = "/"
	if form.is_valid():
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		user = authenticate(email=email, password=password)
		if user is not None:
			messages.success(request, 'Success! Welcome, '+(user.first_name or ""))
			login(request, user)
			return HttpResponseRedirect(next_url)
		else:
			messages.warning(request, 'Invalid username or password.')
			
	context = {
		"form": form,
		"page_name" : "Login",
		"button_value" : "Login",
		"links" : ["register"],
	}
	return render(request, 'auth_form.html', context)

def auth_logout(request):
	logout(request)
	messages.success(request, 'Success, you are now logged out')
	return render(request, 'index.html')

def auth_register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")

	form = RegisterForm(request.POST or None)
	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	if form.is_valid():
		request.session['form'] = form.cleaned_data
		if form.cleaned_data['role'] == 'teacher':
			request.session['role'] = 'teacher'
			return HttpResponseRedirect("/register_teacher")
		elif form.cleaned_data['role'] == 'engineer':
			request.session['role'] = 'engineer'
			return HttpResponseRedirect("/register_engineer")
		elif form.cleaned_data['role'] == 'student':
			return render(request, 'index.html')
		else:
			return render(request, 'index.html')

	return render(request, 'auth_form.html', context)

def register_engineer(request):
	if any(['form' not in request.session,
			'role' not in request.session,
			request.session['role'] != 'engineer']):		
		return HttpRedirect("/")
		messages.success(request, 'we got a')

	last_form = request.session['form']
	form = EngineerForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(
			email=last_form['email'], 
			password=last_form["password2"], 
			first_name=last_form['firstname'],
			last_name=last_form['lastname'])
		messages.success(request, last_form['email'] + ' saved')
		new_user.save()
		new_engineer = Engineer(
			user=new_user,
			alma_mater=form.cleaned_data['alma_mater'],
			about=form.cleaned_data['about'],
			phone_number=form.cleaned_data['phone_number']
		)
		new_engineer.save()	
		login(request, new_user);	
		messages.success(request, 'Success! Your engineer account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)
def register_teacher(request):
	if any(['form' not in request.session,
			'role' not in request.session,
			request.session['role'] != 'teacher']):		
		return HttpRedirect("/")

	last_form = request.session['form']
	form = TeacherForm(request.POST or None)
	if form.is_valid():
		new_user = MyUser.objects.create_user(
			email=last_form['email'], 
			password=last_form["password2"], 
			first_name=last_form['firstname'],
			last_name=last_form['lastname'])
		messages.success(request, last_form['email'] + ' saved')
		new_user.save()
		new_teacher = Teacher(
			user=new_user,
			subject=form.cleaned_data['subject'],
			about=form.cleaned_data['about'],
			phone_number=form.cleaned_data['phone_number']
		)
		new_teacher.save()	
		login(request, new_user);	
		messages.success(request, 'Success! Your Teacher account was created.')
		return render(request, 'index.html')

	context = {
		"form": form,
		"page_name" : "Register",
		"button_value" : "Register",
		"links" : ["login"],
	}
	return render(request, 'auth_form.html', context)

@login_required
def update_profile(request):
	form = UpdateForm(request.POST or None, instance=request.user)
	if form.is_valid():
		form.save()
		messages.success(request, 'Success, your profile was saved!')

	context = {
		"form": form,
		"page_name" : "Update",
		"button_value" : "Update",
		"links" : ["logout"],
	}
	return render(request, 'auth_form.html', context)
