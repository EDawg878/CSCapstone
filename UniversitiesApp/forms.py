"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms
from .models import Teacher

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
	subject = forms.CharField(label='subject', max_length=200)
	about = forms.CharField(label='About', max_length=300)
	phone_number = forms.CharField(label='Phone Number', max_length=20)

class UpdateTeacherForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = ('subject', 'about', 'phone_number')
