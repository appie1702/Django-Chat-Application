from django.db import models
# from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.username


class Room(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    password = models.CharField(max_length=300000, default=None, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Message(models.Model):
    data = models.CharField(max_length=3000000, blank=True)
    date_time = models.DateTimeField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=300, blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.data[:5]
