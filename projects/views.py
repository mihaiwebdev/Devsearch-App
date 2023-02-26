from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import ProjectForm, ReviewFrom
from .models import Project, Tag
from .utils import searchProjects, paginateProjects


# Create your views here.


def projects(request):

    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}

    return render(request, 'projects/projects.html', context)


def singleProject(request, pk):

    project = Project.objects.get(id=pk)

    form = ReviewFrom()

    if request.method == 'POST':
        form = ReviewFrom(request.POST)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.project = project
            feedback.owner = request.user.profile
            feedback.save()

            project.getVoteCount

            messages.success(
                request, 'Your reviews was successfully submitted')

            return redirect('project', pk=project.id)

    context = {'project': project, 'form': form}

    return render(request, 'projects/project-page.html', context)


@login_required(login_url="login")
def createProject(request):

    profile = request.user.profile

    form = ProjectForm()

    if request.method == 'POST':
        newTags = request.POST.get('newTags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, 'Project was added successfully')

            return redirect('user-account')

    context = {'form': form, 'action': 'Create'}

    return render(request, 'projects/project-form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):

    profile = request.user.profile

    project = profile.project_set.get(id=pk)

    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newTags = request.POST.get('newTags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            project = form.save()

            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            messages.success(request, 'Project was updated successfully')

            return redirect('user-account')

    context = {'form': form, 'action': 'Update', 'project': project}

    return render(request, 'projects/project-form.html', context)


@login_required(login_url="login")
def deleteProject(request, pk):

    profile = request.user.profile

    project = profile.project_set.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('user-account')

    context = {'object': project, 'title': project.title}

    return render(request, 'delete-template.html', context)
