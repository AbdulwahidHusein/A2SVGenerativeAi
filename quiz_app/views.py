from django.shortcuts import render
from django.http import JsonResponse
from  quiz_app.api import bard_api

#from file_handler import FileHandler
#import api_request
# Create your views here.

from quiz_app.file_processor import filehandler

def homee(request):
    return render(request, 'home.html')


def home(request):
    error = ''
    if request.method == "POST":
        try:
            uploaded_file = request.FILES['file']
            num_of_questions = request.POST.get('qnumber')
            difficulty = request.POST.get('')
            file_handle = filehandler.FileHandler(uploaded_file)
            spage = request.POST.get('spage')
            epage = request.POST.get('epage')
            
        except:
            error = "error uploading Your file"
    
        file_handle.read_pdf(spage, epage)
        summerised = file_handle.summerized(500, 10)
        #make Apicall
        question = bard_api.generate_question(summerised, num_of_questions, difficulty)
        parsed = bard_api.parse_question(question)

  
  
        return JsonResponse(parsed)
    return render(request, 'home.html')