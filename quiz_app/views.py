from django.shortcuts import render, redirect
from django.http import JsonResponse
from  quiz_app.api import bard_api
from .models import CustomUser
#from file_handler import FileHandler
#import api_request
# Create your views here.

from quiz_app.file_processor import filehandler

def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        carrier= request.POST.get("role")
        gender = request.POST.get("gender")
        
        if password1 == password2:
            user = CustomUser.objects.create(username=email, password=password2,email=email,carrier=carrier,gender=gender )
            #user.save()
            return redirect('quiz')
        else:
            return render(request, 'registration.html', {'error':''})
    return render(request, 'registeration.html')

def home(request):
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        num_of_questions = request.POST.get('qnumber')
        difficulty = request.POST.get('difficulty')
        spage = request.POST.get('spage')
        epage = request.POST.get('epage')
        file_handle = filehandler.FileHandler(uploaded_file)
        
        file_handle.read_file(spage, epage)

        summerised = file_handle.summerized(500, 10)
        #make Apicall
        question = bard_api.generate_question(summerised, num_of_questions, difficulty)
        parsed = bard_api.parse_question(question)

        if parsed:
            return JsonResponse(parsed)
        else:
            return JsonResponse({'error2':'error'})
    return render(request, 'home.html')