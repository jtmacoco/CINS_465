from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('',views.index ),
    path('login/',auth_views.LoginView.as_view()),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('movies/',views.movies_view),
    path('match/',views.match_view),
    path('delete/', views.delete_view),
    path('createProfile/',views.createProfile_view),
    path('profile/',views.profile_view),
    path('chat/',views.chat_view),
    path('<str:username>/',views.user_profile_view,name='username'),

    path('<str:room_name>/', views.room, name='room'),

]
