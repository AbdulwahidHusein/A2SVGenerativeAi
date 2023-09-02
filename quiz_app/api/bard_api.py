import json
import re
import os
from  bardapi import Bard
from django.conf import settings
API_KEY = settings.API_KEY

question_format ={
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

def generate_question(text, number_of_questions, difficulty):
    global API_KEY
    prompt  = f'''generate a quiz contining {number_of_questions} different multiple choice questions with different context containing four choices with {difficulty} difficulty the questions must be returned in the following format {question_format} note the question must be in json format!!! also make sure the explanations must be less than 2 lines important!.
     NOTE only use the following text for the generation of quiz {text}'''
    bard = Bard(token = API_KEY)
    answer = bard.get_answer(prompt)['content']
    return answer
     
def parse_question(text):
  json_data = re.search(r"\{.*\}", text, re.DOTALL).group(0)
  #print(text)
  json_data = json.loads(json_data)
  
  return json_data