"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms
from .models import Student, Teacher, University

class UniversityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    photo = forms.ImageField(label='Photo')
    description = forms.CharField(label='Description', max_length=300)
    website = forms.CharField(label='Website', max_length = 300)
	
class CourseForm(forms.Form):
	tag = forms.CharField(label='Tag', max_length=10)
	name = forms.CharField(label='Name', max_length=50)
	description = forms.CharField(label='Description', max_length=300)

class TeacherForm(forms.Form):
	university = forms.ModelChoiceField(queryset=University.objects.all())
	subject = forms.CharField(label='Subject', max_length=200)
	about = forms.CharField(label='About', max_length=300)
	phone_number = forms.CharField(label='Phone Number', max_length=20)

class UpdateTeacherForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = ('university', 'subject', 'about', 'phone_number')

class StudentForm(forms.Form):
	university = forms.ModelChoiceField(queryset=University.objects.all())
	class_standing = forms.CharField(label='Class Standing', max_length=20)

class UpdateStudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('university', 'class_standing')
