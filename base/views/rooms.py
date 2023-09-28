from django.shortcuts import render, redirect
from ..models import Room, Topic, Message
from ..forms import RoomForm
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


@login_required(login_url='login')
def createRoom(request):
    from_url = request.GET.get(
        'from') if request.GET.get('from') else 'home'

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            private = form.cleaned_data['private']
            if is_guest_user(request.user):
                private = False

            # Separate handling for topic creation
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            room = Room.objects.create(
                host=request.user,
                topic=topic,
                name=name,
                description=description,
                private=private
            )

            room.participants.add(request.user)

            if from_url == 'profile':
                response = redirect(from_url, pk=str(request.user))
                response['Location'] += '?filter=recent'
                return response
            else:
                response = redirect(from_url)
                response['Location'] += '?filter=recent'
                return response
    else:
        form = RoomForm()

    context = {'form': form, 'from_url': from_url,
               'topics': Topic.objects.all()}
    return render(request, 'base/roomform.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):

    from_url = request.GET.get(
        'from') if request.GET.get('from') else 'home'

    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    context = {}
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save(commit=False)
            if is_guest_user(request.user):
                form.private = False

            form.save()

            if from_url == 'profile':
                response = redirect(from_url, pk=str(request.user))
                response['Location'] += '?filter=recent'
                return response

            else:
                response = redirect(from_url)
                response['Location'] += '?filter=recent'
                return response
    else:
        # coudnt get current_topic value for html simply(was instead getting id)

        current_topic = form['topic'].value()
        if current_topic:
            current_topic = Topic.objects.get(id=current_topic)
            context = {'form': form, 'updateRoom': True,
                       'current_topic': current_topic, 'from_url': from_url}
        else:
            context = {'form': form, 'updateRoom': False, 'from_url': from_url}

        return render(request, 'base/roomform.html', context)

    return render(request, 'base/roomform.html', context)


@login_required(login_url='login')
def deleteRoom(request):
    if request.method == 'POST':
        pk = request.POST.get('room_id')
        user = request.POST.get('user')
        if str(request.user) != str(user):
            return HttpResponse('You are not allowed here')
        room = Room.objects.get(id=pk)
        room.delete()
        return JsonResponse({'success': True})


@login_required(login_url='login')
def LeaveRoom(request):
    room_id = request.GET.get('id')
    if room_id:
        try:
            room = Room.objects.get(id=room_id)
            url = 'room/' + room.slug

            if request.user in room.participants.all():
                room.participants.remove(request.user)
                return redirect(url)
            else:
                return redirect(url)

        except Exception as e:
            return HttpResponse('you not in ')

    else:
        return redirect('home')


@login_required(login_url='login')
def JoinRoom(request):
    room_id = request.GET.get('id')
    if room_id:
        try:
            room = Room.objects.get(id=room_id)

            if request.user not in room.participants.all() and room.private == False:
                room.participants.add(request.user)
            return JsonResponse({'success': True})
        except Exception as e:
            return redirect('home')


def Invite(request, code):
    try:
        room = Room.objects.get(Q(invite_code=code) | Q(slug=code))
        if room.private:
            room = None if room.invite_code != code else room
    except Exception as e:
        room = None

    context = {'room': room}
    return render(request, 'base/invite.html', context)


@login_required(login_url='login')
def InviteJoin(request, code):
    try:
        room = Room.objects.get(Q(invite_code=code) | Q(slug=code))
        if room.private:
            if code == room.invite_code:
                room.participants.add(request.user)
                return redirect('room', room.slug)
            else:
                return redirect('home')
        else:
            # room is not private
            room.participants.add(request.user)
            return redirect('room', room.slug)

    except Exception as e:
        return redirect('home')


def InvitePage(request):
    return render(request, 'base/invite_page.html', {})
