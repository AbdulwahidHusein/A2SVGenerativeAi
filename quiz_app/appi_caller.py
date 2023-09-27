import os
from dotenv import load_dotenv
from api import PromptGenerator, OpenAi, BardEx
from api_response import ResponseParser

load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")
OPEN_AI_API_KEY  = os.getenv('OPEN_AI_API_KEY')

class GenerateQuestionRequest:
    
    def __init__(self, document_content, model) -> None:
        self.document_data = document_content
        self.model = model
        self.response = {}
        
    def make_request(self, number_of_questions, difficulty, question_format):

        prompt_generator = PromptGenerator(self.document_data)
        prompt = prompt_generator.make_prompt(number_of_questions,difficulty, question_format)

        if self.model == 'chatgpt':
            open_ai = OpenAi(OPEN_AI_API_KEY)
            generated_questions = open_ai.generate_question(prompt)
            parsed = ResponseParser(generated_questions)
            parsed = parsed.get_json_data()
            return parsed
        
        else:
            bard = BardEx(BARD_API_KEY, '', '')
            generated_questions = bard.get_answer(prompt)
            parsed = ResponseParser(generated_questions)
            parsed = parsed.get_json_data()
            return parsed