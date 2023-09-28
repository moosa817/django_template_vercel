from django.shortcuts import render, redirect
from ..models import Room, UserProfile
from django.db.models import Q
from django.db.models import Count
from guest_user.decorators import allow_guest_user
from django.conf import settings
# Create your views here.


def home(request):

    q = request.GET.get('q') if request.GET.get('q') else ''
    topics_only = request.GET.get(
        'topic') if request.GET.get('q') else ''
    page = int(request.GET.get('page')) if request.GET.get('page') else 1

    order_by = '-updated' if request.GET.get(
        'filter') == 'recent' else 'participants'

    rooms = Room.objects.filter().order_by(order_by)

    one_page = settings.ROOM_PAGE
    end_page = page * one_page
    start_page = end_page - one_page

    if topics_only:
        rooms = rooms.filter(
            Q(topic__name__icontains=q)
        )

    else:
        rooms = rooms.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    if request.user.is_authenticated:
        rooms = rooms.filter(Q(private=False) | Q(
            participants=int(request.user.id)))
    else:
        rooms = rooms.filter(private=False)

    rooms = list(dict.fromkeys(rooms))
    room_count = len(rooms)

    rooms = rooms[start_page:end_page]
    last_page = room_count//one_page + (room_count % one_page > 0)

    context = {'rooms': rooms,
               'q': q, 'topics_only': topics_only, 'room_count': room_count, 'last_page': last_page}

    return render(request, 'base/home.html', context)
