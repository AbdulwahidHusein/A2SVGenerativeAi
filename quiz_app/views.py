from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CustomUser, Message, Quiz, GroupQuiz, ScoreHolder
from .generator import get_question
import json, re
from dateutil import parser

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

@login_required(login_url='login')
def handle_quiz_submit(request):
    id = request.POST.get('id')
    score = request.POST.get('score')
    quiz = Quiz.objects.get(pk=id)
    
    quiz.user_score = score
    quiz.save()
    return JsonResponse({"status":"okay"}, safe=False)


@login_required(login_url='login')
def myquizes(request):
    user = request.user
    quizs = Quiz.objects.all().filter(generated_by= user)
    return render(request, 'my_quizes.html', {"quizes":quizs})
    


def chat(request):
    return render(request, 'chat2.html')



@login_required(login_url='login')
def user_group_quizs(request):
    user = request.user
    group_quizzes = GroupQuiz.objects.filter(joined_members=user)
    return render(request, "joined_group_quizes.html", {"group_quizes":group_quizzes})

def get_group_quiz_info(request, id):
    data = {}
    group_quiz = get_object_or_404(GroupQuiz, pk=id)
    #GroupQuiz.objects.get(pk=id)
    quiz = group_quiz.quiz
    questions = quiz.questions
    questions = re.sub(r"'", '"',questions)
    questions = json.loads(questions)
    group_quiz.quiz.questions = questions#may not be possible but lets try it  
    group_quiz.update_status()
    data['group_quiz'] = group_quiz
    
    #joined_members = group_quiz.joined_members.all()
    scores = ScoreHolder.objects.all().filter(group_quiz=group_quiz).order_by('score')
    data['scores'] = scores
    return render(request, 'group_quiz_comp.html', data)
    
@login_required(login_url='login')   
def handle_join_group(request, id):
    user = request.user
    group_quiz = GroupQuiz.objects.get(pk=id)
    group_quiz.update_status()
    group_quiz.joined_members.add(user)
    score = ScoreHolder(score=0,competitor=user, group_quiz=group_quiz)
    score.save()
    
    return

@login_required(login_url='login')
def create_group_quiz(request):
    user  = request.user
    date_string = "2023-10-16 10:30:00"
    # from datetime import datetime

    # # User-provided inputs
    # user_date = '2023-10-15'  # User-provided date
    # user_time = '14:30:00'    # User-provided time

    # # Current year
    # current_year = datetime.now().year

    # # Combine date, time, and current year
    # combined_datetime_str = f'{current_year}-{user_date} {user_time}'

    # # Create datetime object
    # combined_datetime = datetime.strptime(combined_datetime_str, '%Y-%m-%d %H:%M:%S')

    # # Store combined_datetime in the database or perform other operations
    if request.method == "POST":
        id = request.POST.get('id')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
            
            # Convert datetime strings to datetime objects
        parsed_start_date_time = parser.parse(start_time_str)
        parsed_end_date_time = parser.parse(end_time_str)

        quiz = Quiz.objects.get(pk=id)
        
        group_quiz = GroupQuiz(quiz=quiz, start_time=parsed_start_date_time, end_time=parsed_end_date_time, created_by=user)

        group_quiz.save()
        group_quiz.joined_members.add(user)
        print("time"*100, group_quiz.start_time)
        group_quiz.save()
        
        return redirect('group_quizes')
    quizzes = Quiz.objects.all().filter(generated_by=user)
    return render(request, 'create_group_quiz.html', {'quizzes':quizzes})
    
    
    
    