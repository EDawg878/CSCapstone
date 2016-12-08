"""
CompaniesApp Forms

Created by Jacob Dunbar on 10/3/2016.
"""
from django import forms
from .models import Project

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=200)
    website = forms.CharField(label='Website', max_length=200)
    description = forms.CharField(label='Description', max_length=1000)
    language = forms.CharField(label='Programming Language', max_length=100)
    experience = forms.IntegerField(label='Years of Experience')
    specialty = forms.CharField(label='Specialty', max_length=100)

class UpdateProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('name', 'website', 'description', 'language', 'experience', 'specialty')
