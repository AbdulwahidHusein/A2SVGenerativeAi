from django.urls import path
from . import views
urlpatterns = [
    path('quiz', views.home, name="quiz"),
    path('register', views.user_register, name="register"),
    path('login', views.login, name='login'),
]
