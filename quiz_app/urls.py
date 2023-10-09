from django.urls import path
from . import views

urlpatterns = [
    path('quiz', views.home, name="quiz"),
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name='login'),
    path('test', views.test, name="test"),
    path('chat/<str:query>', views.chat, name='char'),
    path('get_chat/', views.get_chat, name="get_chat"),
    path('logout/', views.user_logout, name="logout"),
    
    
    
    #new paths
    
    path('home', views.home, name="home"),
    path('upload', views.upload, name="upload"),
    path('quiz', views.quiz, name="quiz"),
    path('chat', views.chat, name="chat"),
]