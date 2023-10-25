from django.urls import path
from . import views

urlpatterns = [
   # path('quiz', views.home, name="quiz"),
    path('register', views.user_register, name="register"),
    path('login', views.user_login, name='login'),
    
    path('get_chat/', views.get_chat, name="get_chat"),
    path('logout/', views.user_logout, name="logout"),
    
    
    
    #new paths
    path('quiz/<int:id>', views.get_quiz, name="quiz"),
    path('home', views.home, name="home"),
    path('upload', views.handle_upload, name="upload"),
    path('chat/', views.chat, name="chat"),  
    path('my_quizes', views.myquizes, name='my_quizes'),
    path("update_quiz/", views.handle_quiz_submit, name="handle_quiz_submit"),
    path('update_scoreboard/', views.update_scoreboard, name="update_board"),
     path('get_scoreboard/', views.get_scoreboard, name="get_board"),
    path('group_quiz/<int:id>', views.get_group_quiz_info, name="group_quiz"),
    path('my_group_quizzes', views.user_group_quizs, name="group_quizes"),
    path('create_group_quiz',views.create_group_quiz, name="create_group_quiz"),
    path('join_quiz/<int:id>', views.handle_join_group, name='join_group'),
    path('my_files/', views.get_user_files, name="my_files"),
    path('download_file/<int:id>', views.download_file, name="download_file"),
    path('generate_quiz/<int:id>/', views.generate_quiz_from_uploaded_file, name="generate_quiz"),
]
