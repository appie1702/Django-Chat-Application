from django import forms
from django.contrib.auth import get_user_model
from .models import Room, Message

User = get_user_model()


class JoinRoomForm(forms.Form):
    roomname = forms.CharField(label='Room', max_length=100, required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
        }))
    password = forms.CharField(min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={
                                       "class": "form-control"
                                   }
                               )
                               )

    def clean_roomname(self):
        room = self.cleaned_data.get('roomname')
        qs = Room.objects.filter(name=room)

        if not qs.exists():
            raise forms.ValidationError("This Room doesn't exists.")
        return room

    def clean_password(self):
        room = self.cleaned_data.get('roomname')
        password = self.cleaned_data['password']
        try:
            qs = Room.objects.get(name=room)
        except:
            qs = None
        if qs and not (qs.password == password):
            raise forms.ValidationError("Password is incorrect")
        return password


class CreateRoomForm(forms.Form):
    roomname = forms.CharField(label='Room Name', max_length=100, required=True, widget=forms.TextInput(
        attrs={
            "class": "form-control w-full bg-white rounded border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
        }))
    password = forms.CharField(min_length=6,
                               label='Password',
                               widget=forms.PasswordInput(
                                   attrs={
                                       "class": "form-control"
                                   }
                               )
                               )

    def clean_roomname(self):
        room = self.cleaned_data['roomname']
        qs = Room.objects.filter(name=room)

        if qs.exists():
            raise forms.ValidationError("This Room is already exists.")
        return room


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       "class": "form-control",
                                       "placeholder": "Username",
                                       "id": "username"
                                   }
                               )
                               )

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Email Address",
            "id": "email_address"
        }
    ), required=True)

    password1 = forms.CharField(min_length=6,
                                label='Password',
                                widget=forms.PasswordInput(
                                    attrs={
                                        "class": "form-control",
                                        "id": "user-password1",
                                        "placeholder": "Password"
                                    }
                                ), required=True
                                )
    password2 = forms.CharField(min_length=6,
                                label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={
                                        "class": "form-control",
                                        "id": "user-password2",
                                        "placeholder": "Confirm Password"
                                    }
                                ), required=True
                                )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)

        if qs.exists():
            raise forms.ValidationError("This username already exists.Please pick another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)

        if qs.exists():
            raise forms.ValidationError("This email is already exists.")
        return email

    # def clean_password(self):
    # password1 = self.cleaned_data.get("password1")
    # password2 = self.cleaned_data.get("password2")
    # if password1 and password2 and password1 != password2:
    #    raise forms.ValidationError("Passwords are mismatched")
    # return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(
                                   attrs={
                                       "class": "form-control",
                                       "placeholder": "Username"
                                   }
                               ), required=True
                               )

    password = forms.CharField(label='Password', min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={
                                       "class": "form-control",
                                       "id": "user-password",
                                       "placeholder": "Password"
                                   }
                               ), required=True
                               )

    def clean_username_password(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)

        if not qs.exists():
            raise forms.ValidationError("This is an invalid user")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            qs = User.objects.get(username__iexact=username)
            correct = qs.check_password(password)
            if not correct:
                raise forms.ValidationError("password is incorrect")
        except:
            raise forms.ValidationError("username is incorrect")
        return password

    def __str__(self):
        return self.username
