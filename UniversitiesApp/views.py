"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render

from . import models
from . import forms
from .models import Student
from django.contrib import messages
from AuthenticationApp.models import MyUser
from django.http import HttpResponseRedirect

def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        del_student = request.GET.get('delete_student', -1)
        in_university = models.University.objects.get(name__exact=in_name)
        if del_student >= 0:
            user = MyUser.objects.get(id__exact=del_student)
            student = Student.objects.get(user_id__exact=del_student)
            in_university.members.remove(user)
            in_university.save();
            student.university = None
            student.save()
            messages.success(request, 'Removed student')

        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        return render(request, 'university.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'], 
                                             photo=request.FILES['photo'],  
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated() and request.user.role == 'student':
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        student = Student.objects.filter(user_id=request.user.id)[0]
        student.university = in_university
        student.save()
        request.user.university_set.add(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        return render(request, 'university.html', context)
    return render(request, 'autherror.html')
    
def getCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		is_member = in_course.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse' : is_member,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.CourseForm(request.POST)
			if form.is_valid():
				in_university_name = request.GET.get('name', 'None')
				in_university = models.University.objects.get(name__exact=in_university_name)
				if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
					return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
				new_course = models.Course(tag=form.cleaned_data['tag'],
										   name=form.cleaned_data['name'],
										   description=form.cleaned_data['description'],
										   university=in_university)
				new_course.save()
				in_university.course_set.add(new_course)
				is_member = in_university.members.filter(email__exact=request.user.email)
				context = {
					'university' : in_university,
					'userIsMember': is_member,
				}
				return render(request, 'university.html', context)
			else:
				return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
		else:
			form = forms.CourseForm()
			return render(request, 'courseform.html')
		# render error page if user is not logged in
	return render(request, 'autherror.html')
		
def removeCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.delete()
		is_member = in_university.members.filter(email__exact=request.user.email)
		context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
		return render(request, 'university.html', context)
	# render error page if user is not logged in
	return render(request, 'autherror.html')

def joinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.add(request.user)
		in_course.save();
		request.user.course_set.add(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': True,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def unjoinCourse(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		in_course_tag = request.GET.get('course', 'None')
		in_course = in_university.course_set.get(tag__exact=in_course_tag)
		in_course.members.remove(request.user)
		in_course.save();
		request.user.course_set.remove(in_course)
		request.user.save()
		context = {
			'university' : in_university,
			'course' : in_course,
			'userInCourse': False,
		}
		return render(request, 'course.html', context)
	return render(request, 'autherror.html')

def add_student(request):
    if request.method == 'POST':
        in_name = request.GET.get('name', 'None')
        form = forms.AddStudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['student']
            in_university = models.University.objects.get(name__exact=in_name)
            if request.user.role == 'teacher' or request.user.role == 'admin':
                to_add = MyUser.objects.filter(email__exact=email)
                if to_add.exists():
                    to_add = to_add[0]
                    if to_add.role == 'student':
                        student = Student.objects.get(user_id__exact=to_add.id)
                        in_university.members.add(to_add)
                        in_university.save()
                        student.university_id = in_university.id
                        student.save()
                    else:
                        messages.warning(request, 'User must be a student to be added to the university')
                else:
                    messages.warning(request, 'Email not found')
            else:
                messages.warning(request, 'You must be a teacher to add students')
        return HttpResponseRedirect("/university?name="+in_name)
    return HttpResponseRedirect("/university/all")
