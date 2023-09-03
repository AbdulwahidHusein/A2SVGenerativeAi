from django.shortcuts import render, redirect
from django.http import JsonResponse
from  quiz_app.api import bard_api
from .models import CustomUser
from quiz_app.file_processor import file_handler
#import api_request
# Create your views here.


def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        carrier= request.POST.get("role")
        gender = request.POST.get("gender")
        user = True
        try:
            CustomUser.objects.get(email=email)
        except:
            user = False
        if password1 == password2 and not user:
            user = CustomUser.objects.create(username=email, password=password2,email=email,carrier=carrier,gender=gender, first_name=full_name )
            #user.save()
            return redirect('quiz')
        elif user:
            return render(request, 'registration.html', {'error':'a user with this email already registerd'})
        else:
            return render(request, 'registration.html', {'error':'passord did not match'})
        
    return render(request, 'registeration.html')

def home(request):
    user = request.user
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        num_of_questions = request.POST.get('qnumber')
        difficulty = request.POST.get('difficulty')
        spage = int(request.POST.get('spage'))
        epage = int(request.POST.get('epage'))
        file_handle = file_handler.FileHandler(uploaded_file)
        file_handle.read_file(spage, epage)
        
        summerised = file_handle.summerized()
        #make Apicall
        question = bard_api.generate_question(summerised, num_of_questions, difficulty)
        parsed = bard_api.parse_question(question)

        if parsed:
            return JsonResponse(parsed)
        else:
            return JsonResponse({'error2':'error genrating a response'})
    if user.is_authenticated:   
        return render(request, 'home.html', {"auth":True})
    return render(request, 'home.html', {"auth":False})