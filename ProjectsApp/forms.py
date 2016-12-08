"""
CompaniesApp Forms

Created by Jacob Dunbar on 10/3/2016.
"""
from django import forms

class ProjectForm(forms.Form):
    name = forms.CharField(label='Name', max_length=200)
    website = forms.CharField(label='Website', max_length=200)
    description = forms.CharField(label='Description', max_length=1000)
