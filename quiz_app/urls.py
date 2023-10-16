from django.urls import path
from . import views

urlpatterns = [
   # path('quiz', views.home, name="quiz"),
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name='login'),
    path('chat/<str:query>', views.chat, name='char'),
    path('get_chat/', views.get_chat, name="get_chat"),
    path('logout/', views.user_logout, name="logout"),
    
    
    
    #new paths
    path('quiz/<int:id>', views.get_quiz, name="quiz"),
    path('home', views.home, name="home"),
    path('upload', views.upload, name="upload"),
    path('chat', views.chat, name="chat"),
    path('my_quizes', views.myquizes, name='my_quizes'),
    path("update_quiz/", views.handle_quiz_submit, name="handle_quiz_submit"),
    path('group_quiz/', views.get_quiz, name="quiz"),
]
