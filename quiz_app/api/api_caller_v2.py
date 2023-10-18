import os
import sys
sys.path.append('..')
from dotenv import load_dotenv
from .api_setup_v2 import PromptGenerator, OpenAi
from .parse_response_v2 import ResponseParser

load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")
OPEN_AI_API_KEY  = os.getenv('OPEN_AI_API_KEY')

multiple_choice_question_format = '''
[
9. Why is cybersecurity important?
A. To prevent financial loss
B. To maintain business continuity
C. To protect sensitive data
D. All of the above
CorrectOption: optionD
Explanation: Cybersecurity is crucial to prevent financial loss, maintain business continuity, and protect sensitive data from unauthorized access. It also helps in preventing reputational damage and legal consequences.
$$$$
10. What does the threat landscape in cyberspace include?
A. Malware
B. Phishing attacks
C. Ransomware
D. All of the above
CorrectOption: optionC
Explanation: The threat landscape in cyberspace is constantly evolving and includes various forms of cyber threats like malware, phishing attacks, ransomware, social engineering, network breaches, and more.

]

'''

short_answer_question_format = {
    'questions': [
   {
      "question": "question1"
    },
     {
      "question": "question2"
    },
     {
      "question": "question3"
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
            print(generated_questions)
            parsed = ResponseParser(generated_questions)
            parsed = parsed.get_json_data()
            return parsed




if __name__ == '__main__':
    text = '''
    Testing plays a crucial role in software development, ensuring the quality, reliability, and functionality of the software being developed. It involves systematically evaluating the software against defined criteria to identify defects, errors, and areas for improvement. Here are some key points to consider when it comes to testing in software development:

    Quality Assurance: Testing is an integral part of quality assurance in software development. It helps verify that the software meets the specified requirements, functions as intended, and delivers the expected value to end users.

    Types of Testing: Various types of testing exist, including functional testing, performance testing, security testing, usability testing, compatibility testing, and more. Each type focuses on specific aspects of the software to ensure its effectiveness and reliability.

    Testing Lifecycle: Testing activities are typically carried out throughout the software development lifecycle. It begins with requirements analysis and continues through design, implementation, and maintenance. Testing is iterative, with each cycle building upon previous testing efforts.

    '''



    generator = GenerateQuestionRequest(text, 'chatgpt')
    data = generator.make_request(50, 'medium', 'multiple_choice')

    print(data)