from django.shortcuts import render, redirect
from ..models import Room, Topic, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from guest_user.functions import is_guest_user
# Create your views here.


@login_required
def JoinRoom(request):
    pass


@login_required
def LeaveRoom(request):
    pass
