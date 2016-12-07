"""
CompaniesApp Models

Created by Jacob Dunbar on 10/2/2016.
"""
from django.db import models
from AuthenticationApp.models import MyUser

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to="static/companyimages", default=0)
    description = models.CharField(max_length=300)
    website=models.CharField(max_length=300, default="/")
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
