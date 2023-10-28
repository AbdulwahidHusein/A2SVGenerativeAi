from django.contrib import admin
from .models import CustomUser, Message
# Register your models here.
from .models import *
admin.site.register(CustomUser)
admin.site.register(Message)
admin.site.register(ScoreHolder)
admin.site.register(GroupQuiz)
admin.site.register(Quiz)
admin.site.register(File)