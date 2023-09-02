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
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        file_handle = file_handler.FileHandler(uploaded_file)
        file_handle.read_pdf(5, 10)
        summerised = file_handle.summerized(500, 10)
        #make Apicall
        question = bard_api.generate_question(summerised, 5, 'very hard')
        parsed = bard_api.parse_question(question)

  
  
        return JsonResponse(parsed)
    return render(request, 'home.html')