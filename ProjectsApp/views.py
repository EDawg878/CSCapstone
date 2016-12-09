"""ProjectsApp Views

Created by Harris Christiansen on 10/02/16.
"""
import datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from . import models
from . import forms
from AuthenticationApp.models import Bookmark

def getProjectForm(request):
	if request.user.is_authenticated():
		form = forms.ProjectForm(request.POST or None)
		if form.is_valid():
			new_project = models.Project(
				name = form.cleaned_data['name'],
				description = form.cleaned_data['description'],
				created_at = datetime.datetime.now(),
				updated_at = datetime.datetime.now()
			)
			new_project.save()
			messages.success(request, 'New project created')
			return HttpResponseRedirect('/project/all')
		
		context = {
			"form" : form,
			"page_name" : "Create Project",
			"button_value" : "Create"
		}
		return render(request, 'projectform.html', context)
	return render(request, 'autherror.html')

def editProject(request):
    project_id = request.GET.get('project', 'None')
    project = models.Project.objects.get(id__exact=project_id)
    form = forms.UpdateProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        messages.success(request, 'Success, your project profile was saved!')
        return HttpResponseRedirect('/project/all')

    context = {
        'form' : form,
        'page_name' : 'Edit Project',
        'button_value' : 'Save',
    }
    return render(request, 'projectform.html', context)

def getProjects(request):
	del_project = request.GET.get('delete_project', -1)
	bookmark_project = request.GET.get('bookmark_project', -1)
	if del_project >= 0:
		models.Project.objects.get(id__exact=del_project).delete()
		messages.success(request, 'Deleted project')

	if bookmark_project >= 0:
		project = models.Project.objects.get(id__exact=bookmark_project)
		bookmark = Bookmark(project_name=project.name)
		bookmark.save()
		request.user.bookmarks.add(bookmark)
		request.user.save()
		messages.success(request, 'Added bookmark')
	
	projects_list = models.Project.objects.all()
	return render(request, 'projects.html', {
		'projects': projects_list,
	})

def getProject(request):
	name = request.GET.get('name', 'None')
	project = models.Project.objects.get(name__exact=name)
	is_member = project.members.filter(email__exact=request.user.email)
	context = {
		'project' : project,
		'userIsMember' : is_member
	}
	return render(request, 'project.html', context)

def viewBookmarks(request):
	del_bookmark = request.GET.get('delete_bookmark', 'None')
	if del_bookmark != 'None':
		bookmarks = Bookmark.objects.filter(project_name=del_bookmark)
		for bookmark in bookmarks:
			request.user.bookmarks.remove(bookmark)
			request.user.save()
		messages.success(request, 'Bookmark deleted')
	
	context = {
		"user" : request.user
	}
	return render(request, 'bookmarks.html', context)

def joinProject(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_project = models.Project.objects.get(name__exact=in_name)
		in_project.members.add(request.user)
		in_project.save();
		request.user.project_set.add(in_project)
		request.user.save()
		context = {
			'project' : in_project,
			'userIsMember': True,
		}
		return render(request, 'project.html', context)
	return render(request, 'autherror.html')
    
def unjoinProject(request):
	if request.user.is_authenticated():
		in_name = request.GET.get('name', 'None')
		in_project = models.Project.objects.get(name__exact=in_name)
		in_project.members.remove(request.user)
		in_project.save();
		request.user.project_set.remove(in_project)
		request.user.save()
		context = {
			'project' : in_project,
			'userIsMember': False,
		}
		return render(request, 'project.html', context)
	return render(request, 'autherror.html')
