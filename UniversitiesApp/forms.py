"""
UniversitiesApp Forms

Created by Jacob Dunbar on 11/5/2016.
"""
from django import forms

class UniversityForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    photo = forms.ImageField(label='Photo')
    description = forms.CharField(label='Description', max_length=300)
    website = forms.CharField(label='Website', max_length = 300)
	
class CourseForm(forms.Form):
	tag = forms.CharField(label='Tag', max_length=10)
	name = forms.CharField(label='Name', max_length=50)
	description = forms.CharField(label='Description', max_length=300)

class EngineerForm(forms.Form):
	name = forms.CharField(label='Name', max_length=50)
	alma_mater = forms.CharField(label='Alma Mater', max_length=50)
	about = forms.CharField(label='About', max_length=300)
	phone_number = forms.CharField(label='Phone Number', max_length=20)
