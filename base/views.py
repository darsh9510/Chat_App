from django.shortcuts import render
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
# Create your views here.
from .models import Rooms, topic, Massage,modarator,Anonumous
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import RoomForm
from .codenamegenerator import generate_codenames

# Make the GET request
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Rooms.objects.filter(Q(name__icontains=q)|Q(rtopic__name__icontains=q))
    if request.user.is_authenticated:
        room_u = Rooms.objects.filter(participent=request.user)
    else:
        room_u = Rooms.objects.none()
    context = {'room':room,'count':room.count(),'q':q,'room_u':room_u}

    return render(request, 'home.html', context)

def signin_as_m(request):
    if request.method == 'POST':
        modarator_name = request.POST['modarator_name']
        registration_no = request.POST['modarator_id']
        password = request.POST['password']

        u_exist = User.objects.filter(username=modarator).exists()
        m_exist = modarator.objects.filter(modarator_id=registration_no).exists()
        user = authenticate(username=modarator_name,password=password)
        if m_exist:
            messages.info(request, 'User already exists')
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signin')
        else :
            return redirect('signin')
    return render(request, 'signin_as_m.html')


def signin(request):
    page = 'signin'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('signin')
    context = {'page': page}
    return render(request,'signin.html',context)

def signup(request):
    page = 'signup'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserCreationForm()

    return render(request, 'signin.html', {'form': form})



def room(request, pk):
    room = Rooms.objects.get(id=pk)
    user = Anonumous.objects.filter(anonumous_room = room)
    participant_r = room.participent.all()
    room_u = Rooms.objects.filter(participent=request.user.id)
    messages = Massage.objects.filter(room=room)
    #anonumous = Anonumous.objects.filter(anonumous_room=room)
    user_is_in_room = request.user in room.participent.all()
    context = {'room': room, 'messages': messages,'a_user':user,'room_u':room_u,'user_is_in_room':user_is_in_room,'participant':participant_r}

    if request.method == 'POST':
        if 'join' in request.POST:
            participant_username = request.user.username
            try:
                participant = User.objects.get(username=participant_username)
                room.participent.add(participant)
            except User.DoesNotExist:
                pass
        else:
            message_text = request.POST.get('message')
            user_m = User.objects.filter(username=request.user.username)
            anonumous_e = Anonumous.objects.filter(anonumous_user=request.user).filter(anonumous_room=room).exists()
            if anonumous_e is False:
                a_name = generate_codenames()[0]
                Anonumous.objects.create(anonumous_user=request.user, anonumous_room=room,anonumous_name = a_name) 
            anonumous = Anonumous.objects.filter(anonumous_user=request.user).filter(anonumous_room=room).first()
            message = Massage.objects.create(user=request.user, room=room, text=message_text,a_name = anonumous)
            return redirect('room', pk=room.id)

    return render(request, 'room.html', context)


@login_required(login_url='signin')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        host_user = request.user
        topic_name = request.POST.get('topic')
        topic_exist = topic.objects.filter(name=topic_name).exists()
        type = request.POST.get('type')
        if topic_exist is False:
            topic.objects.create(name=topic_name)
        topic_i = topic.objects.get(name=topic_name)
        topic_id = topic_i.id
        m = request.POST.get('mod')
        m_name = modarator.objects.filter(modarator_id = m).first()
        room = Rooms.objects.create(
            name=room_name,
            host=host_user,
            rtopic=topic_i,
            type=type
        )
        room.participent.add(host_user)
        room.modarator.add(m_name)
        room.participent.add(m_name.modarator_user)
        return redirect('home')
    mod = modarator.objects.all()
    context = {'form':form,'mod':mod}
    return render(request, 'c_room.html',context)


@login_required(login_url='signin')
def deleteRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    if request.method == 'POST':
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='signin')
def removeUser(request,r_id,user):
    if(request.method == 'POST'):
        room = Rooms.objects.get(id=r_id)
        if(room.type==1):
            u = User.objects.get(id=user)
            room.participent.remove(u)
        else:
            u = Anonumous.objects.get(id=user)
            room.participent.remove(u.anonumous_user)
            u.delete()
        return redirect('room',pk = r_id)
    return render(request,'remove.html')

@login_required(login_url='signin')
def deleteMessage(request, pk):
    message = Massage.objects.get(id=pk)
    room = Rooms.objects.get(id=message.room.id)
    modarator_e = modarator.objects.filter(modarator_user=request.user).exists()
    if request.method == 'POST':
        if request.user != message.user and modarator_e is False:
            return HttpResponse('You are not allowed here')
        message.delete()
        return redirect('room',pk = room.id)
    return render(request, 'delete.html', {'obj':message})

@login_required(login_url='signin')
def resetpasswd(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.get(username=username)
        if users.id is not request.user.id:
            return HttpResponse('You are not allowed here')
        users.set_password(password)
        users.save()
        return redirect('signin')
    context = {}
    return render(request, 'resetpasswd.html')
    return render(request, 'resetpasswd.html')

@login_required(login_url='signin')
def logout_u(request):
    logout(request)
    return redirect('home')
