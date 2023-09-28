from django.shortcuts import render, redirect
from ..models import Room, Topic, Message, UserProfile
from ..forms import RoomForm, ProfileCreationForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
# Create your views here.


def LoginPage(request, backend='django.contrib.auth.backends.ModelBackend'):
    page = 'login'
    context = {'page': page}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {'page': page, 'username': username, 'password': password}
        try:
            user = User.objects.get(username=username)
        except:
            try:
                user = UserProfile.objects.get(email=username)
                username = user.username
            except:
                messages.error(request, 'Username or Email does not exist')
                return render(request, 'base/register_login.html', context)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user, backend=backend)
            return redirect('home')
        else:
            messages.error(request, 'Wrong Password')

    return render(request, 'base/register_login.html', context)


def RegisterPage(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        UserForm = UserCreationForm(request.POST)
        ProfileForm = ProfileCreationForm(request.POST)

        if ProfileForm.is_valid() and UserForm.is_valid():
            user = UserForm.save(commit=False)
            user.username = user.username.lower()
            user.save()

            profile = UserProfile.objects.create(
                username=user,
                email=request.POST.get('email').lower(),
            )

            login(request, user, backend=backend)
            return redirect('home')

    else:
        UserForm = UserCreationForm()
        ProfileForm = ProfileCreationForm()

    context = {'UserForm': UserForm, 'ProfileForm': ProfileForm}
    return render(request, 'base/register_login.html', context)


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('home')
