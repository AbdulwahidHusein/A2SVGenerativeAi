import os
import sys
sys.path.append('..')
from dotenv import load_dotenv
from .api_setup import PromptGenerator, OpenAi, BardEx
from .parse_response import ResponseParser

load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")
OPEN_AI_API_KEY  = os.getenv('OPEN_AI_API_KEY')

multiple_choice_question_format = {
    'questions': [
   {
      "question": "question1",
      "optionA": "Choice a",
      "optionB": "Choice B",
      "optionC": "Choice c",
      "optionD": "Choice D",
      "correctOption": "optionA",
      "explanation": "Explanation."
    },
     {
      "questio": "question1",
      "optionA": "Choice a",
      "optionB": "Choice B",
      "optionC": "Choice c",
      "optionD": "Choice D",
      "correctOption": "optionA",
      "explanation": "Explanation."
    }
]
}

short_answer_question_format = {
    'questions': [
   {
      "question": "question1",
      "answer": "Explanation."
    },
     {
      "question": "question2",
      "answer": "Explanation."
    },
     {
      "question": "question3",
      "answer": "Explanation."
    }
     
]
}

class GenerateQuestionRequest:
    
    def __init__(self, document_content, model) -> None:
        self.document_data = document_content
        self.model = model
        
    def make_request(self, number_of_questions, difficulty, mode):
        global multiple_choice_question_format, short_answer_question_format
        
        prompt_generator = PromptGenerator(self.document_data, difficulty)
        if mode == 'multiple_choice':
            prompt = prompt_generator.make_multiple_choice_prompt(number_of_questions, multiple_choice_question_format)
        elif mode == 'short_answer':
            prompt = prompt_generator.make_short_answer_propmt(number_of_questions, short_answer_question_format)
        else:
            prompt = prompt_generator.make_multiple_choice_prompt(number_of_questions, multiple_choice_question_format)
        
        if self.model == 'chatgpt':
            open_ai = OpenAi(OPEN_AI_API_KEY)
            generated_questions = open_ai.generate_question(prompt)
            parsed = ResponseParser(generated_questions, mode)
            parsed = parsed.get_json_data()
            return parsed
        
        else:
            bard = BardEx(BARD_API_KEY)
            generated_questions = bard.get_answer(prompt)
            parsed = ResponseParser(generated_questions, mode)
            parsed = parsed.get_json_data()
            return parsed




if __name__ == '__main__':
    question = '''
    Testing plays a crucial role in software development, ensuring the quality, reliability, and functionality of the software being developed. It involves systematically evaluating the software against defined criteria to identify defects, errors, and areas for improvement. Here are some key points to consider when it comes to testing in software development:

    Quality Assurance: Testing is an integral part of quality assurance in software development. It helps verify that the software meets the specified requirements, functions as intended, and delivers the expected value to end users.

    Types of Testing: Various types of testing exist, including functional testing, performance testing, security testing, usability testing, compatibility testing, and more. Each type focuses on specific aspects of the software to ensure its effectiveness and reliability.

    Testing Lifecycle: Testing activities are typically carried out throughout the software development lifecycle. It begins with requirements analysis and continues through design, implementation, and maintenance. Testing is iterative, with each cycle building upon previous testing efforts.

    '''



    generator = GenerateQuestionRequest(question, 'chatpt')
    data = generator.make_request(5, 'medium', 'multiple_choice')

    print(data)