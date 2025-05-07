from django.shortcuts import render
from .models import Message, Room
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

def create_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        room, created = Room.objects.get_or_create(name=room_name)
        return redirect('room', room_name=room.name)
    return render(request, 'chat/create_room.html')

def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)

    messages = Message.objects.filter(room__name=room_name).order_by('timestamp')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages,
    })