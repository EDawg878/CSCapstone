"""
UniversitiesApp Models

Created by Jacob Dunbar on 11/5/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser
from ProjectsApp.models import Project

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="static/universityimages", default=0)
    description = models.CharField(max_length=300)
    website = models.CharField(max_length=300, default="/")
    members = models.ManyToManyField(MyUser)
    
    def __str__(self):
        return self.name
	
class Course(models.Model):
	tag = models.CharField(max_length=10)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=300)
	university = models.ForeignKey(University, on_delete=models.CASCADE)
	members = models.ManyToManyField(MyUser)

	def __str__(self):
		return self.name

class Engineer(models.Model):
	name = models.CharField(max_length=50)
	alma_mater = models.CharField(max_length=50)
	about = models.CharField(max_length=300)
	phone_number = models.CharField(max_length=20)
	projects = models.ManyToManyField(Project)

	def __str__(self):
		return self.name
