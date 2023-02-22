from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, Profileform, SkillForm
from .utils import searchUsers, paginateProfiles


# Create your views here.
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')

        else:
            messages.error(request, 'Bad Credentials')

    context = {'page': page}

    return render(request, 'users/login-register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()

            user.save()

            messages.success(request, 'User account was created')

            login(request, user)

            return redirect('edit-account')

        else:
            messages.error(request, 'Error has occurred during registration')

    context = {'page': page, 'form': form}

    return render(request, 'users/login-register.html', context)


def profiles(request):

    profiles, search_query = searchUsers(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):

    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact='')
    otherSkills = profile.skill_set.filter(description='')

    context = {'profile': profile, 'topSkills': topSkills,
               'otherSkills': otherSkills}

    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profile

    context = {'profile': profile}

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):

    profile = request.user.profile

    form = Profileform(instance=profile)

    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('user-account')

    context = {'form': form}

    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request):

    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully')

            return redirect('user-account')

    context = {'form': form, 'action': 'Create'}

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated')

            return redirect('user-account')

    context = {'form': form, 'action': 'Update'}

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted!')

        return redirect('user-account')

    context = {'title': skill.name}

    return render(request, 'delete-template.html', context)
