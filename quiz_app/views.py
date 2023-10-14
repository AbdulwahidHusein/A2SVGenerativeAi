from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Message, Quiz
from .generator import get_question
import json, re

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try: 
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid login credentials.'})
        except ObjectDoesNotExist:
            return render(request, 'login.html', {'error': "Naah, we don't know you. Signup."})
    return render(request, 'login.html')

def user_register(request):
    if request.method == "POST":
        full_name = request.POST.get("fullname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        carrier = request.POST.get("profession")
        gender = request.POST.get("gender")
        
        try:
            existing_user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            existing_user = None
        
        if password1 == password2 and not existing_user:
            user = CustomUser(username=email, email=email, carrier=carrier, gender=gender, first_name=full_name)
            user.set_password(password2)
            user.save()
            login(request, user)
            return redirect('home')
        elif existing_user:
            return render(request, 'registeration.html', {'error': 'A user with this email is already registered.'})
        else:
            return render(request, 'registeration.html', {'error': 'Passwords did not match.'})
        
    return render(request, 'registeration.html')




def get_chat(request):
    user_query = request.GET.get('query')
    user = request.user
    chats = Message.objects.all().filter(user=user).order_by('-sent_date')[:6]
    last_3_chats= chats
    response = 'this is response'#bard_api.gpt_chat_session(last_3_chats, user_query)
    #print('sddddddddddddddddddddddddddddddddddddddddddddddddd'+user_query)
    #ask_bard(user_query)
    # Process the user_query and generate the chat response
    #chat_response = process_chat_query(user_query)
    message1  = Message.objects.create(user=user, text=user_query, is_recieved = False)
    message1.save()
    message2  = Message.objects.create(user=user, text=response, is_recieved = True)
    message2.save()
    res = {}
    res['answer'] = response
    return JsonResponse(res)


@login_required(login_url='login')
def chat(request, query):
    user = request.user
    chats = Message.objects.all().filter(user=user).order_by('-sent_date')[:10]
    #answer = ask_bard(query)
    last_3_chats = chats
    if len(last_3_chats) > 6:
        last_3_chats = last_3_chats[:6]     
    response = 'this is response' #bard_api.gpt_chat_session(last_3_chats, query)
    
    if response:
        message1  = Message.objects.create(user=user, text=query, is_recieved = False)
        message1.save()
        message2  = Message.objects.create(user=user, text=response, is_recieved = True)
        message2.save()
       
    return render(request, 'chat.html', {'prev_chats':chats, 'response':response})


def user_logout(request):
    logout(request)
    return redirect('login')



def home(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        context['auth'] = True
    else:
        context['auth'] = False
    return render(request, 'home2.html', context)


@login_required(login_url='login')
def upload(request):
    user = request.user
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        num_of_questions = request.POST.get('qnumber')
        difficulty = request.POST.get('difficulty')
        spage = int(request.POST.get('spage'))
        epage = int(request.POST.get('epage'))
        comment = request.POST.get('additional_comment')
        
        questions = get_question(uploaded_file, 5, difficulty, spage, epage, 'multiple_choice', 'chatgpt')
        print(questions)
        title = questions['questions'][0]['question']
        quiz = Quiz.objects.create(generated_by=user, questions=str(questions),size=5, title=title)
        quiz.save()
        #redirect_url = 'quiz/?questions={}'.format(questions['questions'])
        return render(request, 'quiz3.html', {'questions':questions['questions'], 'id':quiz.id})
    
    return render(request, 'upload.html')

def get_quiz(request, id):
    user = request.user
    quiz = Quiz.objects.get(pk=id)
    if quiz.generated_by.id == user.id:
        questions = quiz.questions
        questions = re.sub(r"'", '"',questions)
        questions = json.loads(questions)
        return render(request, 'quiz3.html', {'questions':questions['questions'], 'id':quiz.id})
    
    quizs = Quiz.objects.all().filter(generated_by= user)
    return render(request, 'my_quizes.html', {"quizes":quizs})
    

def handle_quiz_submit(request, id):
    quiz = Quiz.objects.get(pk=id)
    score = request.GET.get(score)
    quiz.user_score = score
    quiz.save()
    return JsonResponse({"saved"})

@login_required(login_url='login')
def myquizes(request):
    user = request.user
    quizs = Quiz.objects.all().filter(generated_by= user)
    return render(request, 'my_quizes.html', {"quizes":quizs})
    


def chat(request):
    return render(request, 'chat2.html')