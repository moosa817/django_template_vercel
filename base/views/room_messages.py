from django.shortcuts import render, redirect
from ..models import Room, UserProfile, Message
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
# Create your views here.
from django.http import HttpResponseNotFound
from django.conf import settings
from django.core import serializers
from ..templatetags.mytags import pfp_url


def room(request, pk):

    try:
        room = Room.objects.get(slug=pk)
    except Exception as e:
        return HttpResponseNotFound("<h1 style='text-align:center'>Room Not Found<h1>")

    room_messages = room.message_set.all().order_by(
        '-created')[:settings.MESSAGE_ROOM]
    room_messages = reversed(room_messages)

    participants = room.participants.filter()

    if request.user not in participants and room.private:
        return redirect('home')

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}

    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def deleteMessage(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        if pk:
            message = Message.objects.get(id=pk)
            if request.user != message.user:
                return JsonResponse({'success': False})
            else:
                message.delete()
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


@login_required(login_url='login')
def EditMessage(request):

    if request.method == 'POST':
        msg_id = request.POST.get('msg_id')
        new_msg = request.POST.get('new_msg')

        if msg_id and new_msg:
            msg = Message.objects.get(id=msg_id)

            if request.user != msg.user or msg.body == new_msg:
                return JsonResponse({'success': False})
            else:
                msg.body = new_msg
                msg.edited = True
                msg.save()
                return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def LoadMessages(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        last_msg_no = int(request.POST.get('last_msg_no')) + 1

        room = Room.objects.get(id=room_id)

        room_messages = room.message_set.all().order_by(
            '-created')[last_msg_no:last_msg_no+settings.MESSAGE_ROOM]
        # room_messages = reversed(room_messages)

        messages_list = []
        for message in room_messages:
            message_data = {
                'id': message.id,
                'username': message.user.username,
                'body': message.body,
                'edited': message.edited,
                'created': message.created,
                'CurrentUser': True if request.user == message.user else False,
                'pfp':  pfp_url(message.user)
            }
            messages_list.append(message_data)

        return JsonResponse(messages_list, safe=False)

    return JsonResponse({'success': False})
