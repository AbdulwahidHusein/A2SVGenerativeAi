from django.shortcuts import render
from django.http import JsonResponse
from  quiz_app.api import bard_api
from  bardapi import Bard
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv("BARD_API_KEY")

#from file_handler import FileHandler
#import api_request
# Create your views here.

from quiz_app import file_handler

def homee(request):
    return render(request, 'home.html')


def home(request):
    question_format = {
	"JS": [{
			"id": 1,
			"question": "Question number 1",
			"options": [
				"option a", "option b", "option c", "option d"
			],
			"answer": "option c",
			"score": 0,
			"status": "",
			"user_answer": "",
			"explanation": "brief explanation"
		},
		{
			"id": 2,
			"question": "Question number 2",
			"options": [
				"option a", "option b", "option c", "option d"
			],
			"answer": "option c",
			"score": 0,
			"status": "",
			"user_answer": "",
			"explanation": "brief explanation"
		}

	]
}
    if request.method == "POST":
        uploaded_file = request.FILES['file']
        file_handle = file_handler.FileHandler(uploaded_file)
        file_handle.read_pdf(5, 10)
        summerised = file_handle.summerized(500, 10)
        #make Apicall
        question = bard_api.generate_question(summerised, 5, 'very hard', api_key)
        parsed = bard_api.parse_question(question)

  
  
        return JsonResponse(parsed)
    return render(request, 'home.html')