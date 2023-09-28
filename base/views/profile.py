from django.contrib.auth import password_validation
from django.forms import ValidationError
from django.shortcuts import render, redirect
from ..models import Room, Topic, Message, UserProfile
from ..forms import ProfileEditform, CustomUserChangeForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
# Create your views here.
from guest_user.decorators import regular_user_required


def Profile(request, pk):
    user = User.objects.get(username=pk)

    order_by = '-updated' if request.GET.get(
        'filter') == 'recent' else 'participants'

    rooms = Room.objects.filter().order_by(order_by)

    rooms = rooms.filter(host=user)

    context = {'user': user, 'rooms': rooms}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def JoinedRooms(request):
    user_id = request.user.id

    rooms = Room.objects.filter(participants=user_id)

    order_by = '-updated' if request.GET.get(
        'filter') == 'recent' else 'participants'

    rooms = rooms.filter().order_by(order_by)

    context = {'rooms': rooms}
    return render(request, 'base/joined_rooms.html', context)


@regular_user_required
def AccountSettings(request):

    def get_initials():
        profile = UserProfile.objects.filter(username=request.user)
        profile_dict = dict(profile.values()[0])
        profile_dict.pop('id')

        if profile_dict['pfp'] == '/images/guest.webp':
            profile_dict['pfp'] = '/static/img/guest.webp'

        return profile_dict

    ProfileForm = ProfileEditform(initial=get_initials())
    userForm = CustomUserChangeForm(instance=request.user)

    if request.method == 'POST':

        profile = UserProfile.objects.get(username=request.user)
        ProfileForm = ProfileEditform(
            request.POST, request.FILES, instance=profile)
        if ProfileForm.is_valid():
            ProfileForm.save()
            ProfileForm = ProfileEditform(initial=get_initials())

        userForm = CustomUserChangeForm(request.POST, instance=request.user)
        if userForm.is_valid():
            # Check if the old password matches before updating
            old_password = userForm.cleaned_data.get('old_password')
            new_password = userForm.cleaned_data.get('new_password')

            if old_password:
                if request.user.check_password(old_password):
                    if not new_password:
                        userForm.add_error(
                            'new_password', "New password can't be empty")
                    elif new_password == old_password:
                        userForm.add_error(
                            'new_password', "New password can't be the same as old one")
                    else:
                        try:
                            password_validation.validate_password(new_password)
                        except ValidationError as e:
                            userForm.add_error(
                                'new_password', e)

                        else:
                            request.user.set_password(new_password)
                            request.user.save()
                            update_session_auth_hash(request, request.user)
                            messages.success(
                                request, 'Password Sucessfully Changed')

                else:
                    # Old password is incorrect, show an error message
                    userForm.add_error(
                        'old_password', 'Old password is incorrect.')
                    context = {'ProfileForm': ProfileForm,
                               "userForm": userForm}
                    return render(request, 'base/account_settings.html', context)

            userForm.save()
            # Redirect to the user's profile page after editing
            return redirect('account')

    context = {'ProfileForm': ProfileForm, "userForm": userForm}
    return render(request, 'base/account_settings.html', context)
