from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('room/<str:room>', views.room, name='room'),
    path('into/send', views.send, name='send'),
    path('getmessages/into/<str:room>', views.getmessages, name='getmessages'),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('deleteroom/<str:room>', views.delete_room, name='deleteroom'),
    path('token',views.token_view, name='token'),
    path('verify/<auth_token>',views.verify_email, name='verify'),
    path('error',views.error_view, name='error')
]
