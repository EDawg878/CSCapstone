"""GroupsApp Views
Created by Naman Patwari on 10/10/2016.
"""
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect

from . import models
from . import forms
from .forms import AddProjectForm, AddMemberForm
from CommentsApp.models import Comment
from CommentsApp.forms import CommentForm
from AuthenticationApp.forms import MyUser

def getGroups(request):
    if request.user.is_authenticated():
        del_group = request.GET.get('delete_group', -1)
        if del_group >= 0:
            models.Group.objects.get(id__exact=del_group).delete()
            messages.success(request, 'Deleted group')
        groups_list = models.Group.objects.all()
        context = {
           'groups' : groups_list
        }
        return render(request, 'groups.html', context)
    # render error page if user is not logged in
        return render(request, 'autherror.html')

def getGroup(request):
    if request.user.is_authenticated():
        del_comment = request.GET.get('delete_comment', -1)
        if del_comment >= 0:
            return delete_comment(request)

        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        comments_list = Comment.objects.filter(group_id = in_group.id)
        context = {
            'group' : in_group,
            'userIsMember': is_member,
            'comments' : comments_list
        }
        return render(request, 'group.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupForm(request):
    if request.user.is_authenticated():
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getGroupFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.GroupForm(request.POST)
            if form.is_valid():
                if models.Group.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'groupform.html', {'error' : 'Error: That Group name already exists!'})
                new_group = models.Group(name=form.cleaned_data['name'], description=form.cleaned_data['description'])
                new_group.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'groupformsuccess.html', context)
        else:
            form = forms.GroupForm()
        return render(request, 'groupform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def joinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.add(request.user)
        in_group.save();
        comments_list = Comment.objects.filter(group_id = in_group.id)
        request.user.group_set.add(in_group)
        request.user.save()
        context = {
            'comments' : comments_list,
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')
    
def unjoinGroup(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        in_group.members.remove(request.user)
        in_group.save();
        request.user.group_set.remove(in_group)
        request.user.save()
        comments_list = Comment.objects.filter(group_id = in_group.id)
        context = {
                     'comments': comments_list,
            'group' : in_group,
            'userIsMember': False,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def add_project(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        data = {
               'project': in_group.project,
        }
        form = AddProjectForm(request.POST or None)
        if form.is_valid():
               in_group.project = form.cleaned_data['project']
               in_group.save()
        comments_list = Comment.objects.filter(group_id = in_group.id)
        context = {
                     'comments' : comments_list,
            'group' : in_group,
            'userIsMember': True,
        }
        return render(request, 'group.html', context)
    return render(request, 'autherror.html')

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            in_name = request.GET.get('name', 'None')
            in_group = models.Group.objects.get(name__exact=in_name)
            is_member = in_group.members.filter(email__exact=request.user.email)
            new_comment = Comment(
                          user = request.user,
                          group = in_group, 
                          comment=form.cleaned_data['comment'])
            new_comment.save()
            comments_list = Comment.objects.filter(group_id = in_group.id)
            context = {
              'group' : in_group,
              'userIsMember': is_member,
                     'comments' : comments_list
            }
            return render(request, 'group.html', context)
        else:
            form = CommentForm()
    return render(request, 'group.html')

def delete_comment(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_group = models.Group.objects.get(name__exact=in_name)
        is_member = in_group.members.filter(email__exact=request.user.email)
        comment_id = request.GET.get('delete_comment', -1)
        comment = Comment.objects.get(id__exact=comment_id)
        if request.user.role == 'admin' or comment.user_id == request.user.id:
            comment.delete()
            messages.success(request, 'Deleted comment')
            comments_list = Comment.objects.filter(group_id = in_group.id)
            context = {
                'group' : in_group,
                'userIsMember': is_member,
                'comments' : comments_list
            }
            return render(request, 'group.html', context)
    return render(request, 'index.html')

def add_member(request):
    if request.method == 'POST':
        in_name = request.GET.get('name', 'None')
        form = AddMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['member']
            in_group = models.Group.objects.get(name__exact=in_name)
            is_member = in_group.members.filter(email=request.user.email)
            if is_member.exists() or request.user.role == 'admin':
                to_add = MyUser.objects.filter(email__exact=email)
                if to_add.exists():
                    to_add = to_add[0]
                    if to_add.role == 'student':
                        in_group.members.add(to_add)
                        in_group.save()
                        to_add.group_set.add(in_group)
                        to_add.save()
                    else:
                        messages.warning(request, 'User must be a student to be added to the group')
                else:
                    messages.warning(request, 'Email not found')
            else:
                messages.warning(request, 'You must be a member of the group to add others')  
        return HttpResponseRedirect("/group?name="+in_name)
    return HttpResponseRedirect("/group/all")
