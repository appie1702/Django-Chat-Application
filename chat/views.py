import uuid

from django.shortcuts import render, redirect
from chat.models import Room, Message, Profile
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, get_user_model
from .forms import LoginForm, RegisterForm, JoinRoomForm, CreateRoomForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

User = get_user_model()


# Create your views here.
def index(request):
    return render(request, "index.html")


@login_required
def home(request):
    if request.method == "POST":
        if request.POST.get("form_type") == "formOne":
            form1 = CreateRoomForm(request.POST or None)
            form2 = JoinRoomForm()
            if form1.is_valid():
                room = form1.cleaned_data['roomname']
                password = form1.cleaned_data['password']
                qs = Room.objects.filter(name=room)
                if qs.exists():
                    messages.error(request, "This Room Name is already exists.")
                else:
                    room_space = Room.objects.create(name=room, admin=request.user, password=password)
                    room_space.save()
                    url = '/room/' + room
                    return HttpResponseRedirect(url)

        elif request.POST.get("form_type") == "formTwo":
            form1 = CreateRoomForm()
            form2 = JoinRoomForm(request.POST or None)
            if form2.is_valid():
                room = form2.cleaned_data.get('roomname')
                password = form2.cleaned_data.get('password')

                qs = Room.objects.filter(name=room, password=password)

                if not qs.exists():
                    messages.error(request, "RoomName and Password are incorrect or Room doesn't exists.")

                else:
                    url = '/room/' + room
                    return HttpResponseRedirect(url)

        return render(request, 'home.html', {"form1": form1, "form2": form2})

    else:
        form1 = CreateRoomForm()
        form2 = JoinRoomForm()
        return render(request, 'home.html', {"form1": form1, "form2": form2})


@login_required
def room(request, room):
    room_details = Room.objects.filter(name=room).first()
    username = request.user.username
    return render(request, 'room.html', {
        'room': room,
        'room_details': room_details,
        'username': username
    })


def send(request):
    room_id = request.POST['room_id']
    message = request.POST['message']
    username = request.POST['username']
    new_message = Message(data=message, date_time=datetime.now(), user=User.objects.get(username=username),
                          username=username,
                          room=Room.objects.get(id=room_id))
    new_message.save()
    return HttpResponse('Message sent succesfully')


def getmessages(request, room):
    room_details = Room.objects.filter(name=room).first()
    messages = Message.objects.filter(room=room_details)
    return JsonResponse({"messages": list(messages.values())})


def delete_room(request, room):
    room_object = Room.objects.filter(name=room).first()
    if room:
        if room_object.admin == request.user:
            room_object.delete()
            messages.success(request, "Room successfully deleted!!")
            return redirect("/home")
        else:
            messages.error(request, "As you are not the admin of this room,You are not allowed to delete this room.")
            return redirect("/room/" + room)
    else:
        messages.error(request, "Something went wrong. Try after sometime.")
        return redirect("/room/" + room)


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            messages.error(request, "Passwords are mismatched.Enter the correct password.")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password2)
        except:
            user = None
        if user != None:
            profile_obj=Profile.objects.create(user=user,auth_token=str(uuid.uuid4()))
            profile_obj.save
            login(request, user)
            messages.success(request, "You have been successfully logged in.")
            return redirect('/home')
        else:
            request.session['register_error'] = 1
            messages.error(request, "Something went wrong.Retry again after sometime.")
    return render(request, "registration_page.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user != None:

                login(request, user)
                messages.success(request, "You have been successfully logged in.")
                return redirect('/home')
            else:
                request.session['invalid_user'] = 1
                messages.error(request, "username or password is incorrect")
                # return render(request, 'login_page.html', {"form": form})
                return redirect("login")
        return render(request, 'login_page.html', {"form": form})

    else:
        return render(request, 'login_page.html', {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("login")
