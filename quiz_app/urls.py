from django.urls import path
from . import views
urlpatterns = [
    path('quiz', views.home, name="quiz"),
]
