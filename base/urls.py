from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('room/<str:pk>',views.room,name='room'),
    path('createroom',views.createRoom,name='createRoom'),
    path('delete/<str:pk>', views.deleteRoom, name='delete'),
    path('remove/<str:r_id>/<str:user>',views.removeUser, name='remove'),
    path('deletemsg/<str:pk>', views.deleteMessage, name='deletemsg'),
    path('logout', views.logout_u, name='logout'),
    path('resetpasswd', views.resetpasswd, name='resetpasswd'),
    path('sign_as_moderator',views.signin_as_m,name='sign_as_moderator'),
   ]
