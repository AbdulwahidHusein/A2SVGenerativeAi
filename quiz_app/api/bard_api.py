import json
import re
from  bardapi import Bard
import requests
from django.conf import settings

API_KEY = "awiOMKnMNUhtyriLGS_hQHrZNqmNXcHD6tdTUmw7BjBaKPMr3BVv6IwxlkUGi0sUrfKyMw."
import openai
openai.api_key = "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"


session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", API_KEY) 


question_format ={
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

class PromptGenerator:
    
    def __init__(self, text_data):
        self.text = text_data
        self.prompt = ""
        
    def make_prompt(self, number_of_questions, difficulty, question_format):
        prompt  = f'''Dear AI Model,
            Please generate a quiz that consists of {number_of_questions} different multiple-choice questions. Each question should have a unique context and four choices. Set the difficulty level to {difficulty}. The questions must be returned in the following format: {question_format}. 

            Please note that each question, answer, choice, and explanation should be limited to one line. It is important to ensure that all items are quoted to avoid JSON errors. Do not use quoted words that may interfere with the string's quotation. Remember to quote each item properly.

            The question itself should be a valid JSON format with appropriate quotes and commas. The correct option should be written as "option" followed by the option letter, e.g., optionA.

            Please use the provided text to generate the quiz, along with this note.

            Thank you for your assistance in generating the quiz.

            Sincerely,
            PromptGenerator Class'''
        self.prompt = prompt
        return prompt
        

class OpenAi:

    def __init__(self, API_KEY):
        self.api_key = API_KEY
        openai.api_key = self.api_key
        
    def chat(history, query):
        conversation_history = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        for chat in history:
            if chat.is_recieved:
                hist = {'role':'assistant', 'content':chat.text}
                conversation_history.append(hist)
            else:
                hist = {'role':'user', 'content':chat.text}
                conversation_history.append(hist)
        conversation_history.append({'role':'user','content':query})
        
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages = conversation_history,
        )
        generated_response = completion.choices[0].message["content"]
        return generated_response
    
    def generate_question(prompt):
        prompt_token_length = len([w for w in prompt.split()])
        max_tokens = 3500 - prompt_token_length
        parameters = {
            'model': 'text-davinci-003',  # Choose the model you want to use
            'prompt': prompt,
            'max_tokens': max_tokens,  # Adjust the length of the generated reply as needed
            'temperature': 0.7,  # Adjust the temperature to control the randomness of the output
            'n': 1,  # Generate a single reply
            'stop': None,  # You can specify a stop sequence to control the length of the completion
        }
        
        
class BardEx:
    def __init__(self, API_KEY, session, conversation_id) -> None:
        self.api_key = API_KEY
        self.conversation_id = conversation_id
        self.session = session
        self.bard = Bard(API_KEY=self.api_key, session=self.session, conversation_id=self.conversation_id)
        
    def get_answer(self, question):
        answer = self.bard.get_answer(question)
        return answer['content']



def gpt_chat_session(last_3_chats, query):
    conversation_history = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    for chat in last_3_chats:
        if chat.is_recieved:
            hist = {'role':'assistant', 'content':chat.text}
            conversation_history.append(hist)
        else:
            hist = {'role':'user', 'content':chat.text}
            conversation_history.append(hist)
    conversation_history.append({'role':'user','content':query})
    
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = conversation_history,
    )
    generated_response = completion.choices[0].message["content"]
    return generated_response


# maximum token length 1250

def make_prompt(text, number_of_questions, difficulty):
    prompt  = f'''generate a quiz contining {number_of_questions} different multiple choice questions with 
    different context containing four choices with {difficulty} difficulty the questions must be returned in 
    the following format {question_format} note the 
    question must be as in the given json format!!! also make sure each questions, choices and explanation, answer  must be not more than 1 line important!.
 aditionally please make sure that each question, answer, choice and explanation is quoted so that it doest raise json error and never use quoted words since it intrupts the string's quotation. dont forget to quote each items.
     Json error when converted to JSON object. importan the question should be json parsable!!! Text for generation of the quiz: {text}---only use this note and the question should be a valid json with appropirate quotes and commas. the correct option should be written as option followed by option letter like optionA'''
    #print(prompt)

    return prompt

def generate_gpt_question(prompt, user_id):
    prompt_token_length = len([w for w in prompt.split()])
    max_tokens = 3500 - prompt_token_length
    parameters = {
        'model': 'text-davinci-003',  # Choose the model you want to use
        'prompt': prompt,
        'max_tokens': max_tokens,  # Adjust the length of the generated reply as needed
        'temperature': 0.7,  # Adjust the temperature to control the randomness of the output
        'n': 1,  # Generate a single reply
        'stop': None,  # You can specify a stop sequence to control the length of the completion
    }

    # Call the OpenAI API to generate the reply
    response = openai.Completion.create(**parameters)
    reply = response.choices[0].text.strip()
    
    #bard = Bard(token = API_KEY, session=session, conversation_id=f'c_1f04f{str(user_id).zfill(3)}a788e6e4')
    #answer = bard.get_answer(prompt)['content']
    return reply

def generate_bard_question(prompt, user_id):
    global API_KEY, question_format, session
    bard = Bard(token = API_KEY, session=session, conversation_id=f'c_1f04f{str(user_id).zfill(3)}a788e6e4')
    answer = bard.get_answer(prompt)['content']
    return answer
    

def process_response(response_text):
    # Extract the JSON object from the response text
    match = re.search(r'{(.+)}', response_text, re.DOTALL)
    if match:
        json_text = match.group(1)
    else:
        raise ValueError("Invalid response text. JSON object not found.")
    #replace any single quote by double quote
    json_text = '{'+json_text+'}'
    
    json_text = re.sub(r"'", '"', json_text)
    #ensure there is quote after colon
    json_text = re.sub(r":(?!(\[| \[|\"| \"|\]))", ':"', json_text)
    #replace any newline by space
    
    #replace words loke don't and didn't
    
    json_text = re.sub(r"(\b\w+)\"(\w+\b)", r"\1 \2", json_text)
    
    #json_text = re.sub(r'"(?:\s*,\s*|\s*,\s*)\n', ' ', json_text)
    
    #replace all new lines thet intrupts the string 
    #json_text = re.sub(r"\n(?!question|optionA|optionB|optionC|optionD|correctOption|explanation|\})", ' ', json_text)
    
    #add comma before newline 
    json_text = re.sub(r"(?<!,|\]|\{|\[)(?<!\n)(?!\s*(question|optionA|optionB|optionC|optionD|correctOption|explanation|\{|\[|\}|\]))\n", ',\n', json_text)# Convert the JSON object to a Python dictionary
    
    print(json_text)
    try:
        data = json.loads(json_text)
    except Exception as e:
        print(e)

    # Correct the format of the 'correctOption' field
    for question in data['questions']:
        if 'correctOption' in question and len(question['correctOption'].strip()) == 1:
            letter = question['correctOption']
            letter = letter.strip()
            option_key = 'option' + letter.upper()
            if option_key in question:
                question['correctOption'] = option_key

    return data


if __name__ == '__main__':
    text = '''

    Cells are the fundamental building blocks of life, existing in a wide variety of organisms ranging from simple single-celled organisms to complex multicellular organisms. They are incredibly diverse in their structure, function, and specialization, yet they share common features that are essential to their existence.

At the core of every cell is the cell membrane, a selectively permeable barrier that separates the cell from its environment and regulates the entry and exit of molecules. Within the cell, there is a fluid called the cytoplasm, which houses numerous organelles, including the nucleus, mitochondria, endoplasmic reticulum, Golgi apparatus, and more. These organelles work together to carry out various functions necessary for the cell's survival and overall functioning.

The nucleus, often referred to as the cell's control center, contains the genetic material in the form of DNA. DNA carries the instructions that dictate the cell's activities, including growth, development, and reproduction. Surrounding the nucleus is the cytoplasm, where many essential cellular processes occur.

Mitochondria, known as the powerhouses of the cell, generate energy by converting nutrients into ATP through cellular respiration. The endoplasmic reticulum plays a role in protein synthesis and lipid metabolism. The Golgi apparatus modifies, sorts, and packages proteins for transport to their intended destinations within or outside the cell.

Cells are highly specialized, with different types of cells carrying out specific functions within an organism. In multicellular organisms, cells often organize into tissues, which further specialize to form organs and organ systems. These cells and tissues work collaboratively to maintain the overall health and functionality of the organism.

The field of cell biology encompasses the study of cells, their structure, function, and interactions. It explores topics such as cell division, cellular signaling, cell metabolism, cellular communication, and the mechanisms underlying various cellular processes. Cell biology has far-reaching implications in fields like medicine, genetics, developmental biology, neurobiology, and many others.

Understanding cells is crucial to unraveling the mysteries of life. By studying cells, scientists gain insights into the mechanisms that drive growth, development, disease, and the overall functioning of living organisms.

In summary, cells are the basic units of life, exhibiting remarkable diversity and specialization. They play a fundamental role in the functioning of organisms, and the study of cells provides valuable knowledge across various scientific disciplines.'''

    prompt = make_prompt(text, 50, 'medium')
    
    quiz = generate_gpt_question(prompt, 1)
    print(process_response(quiz))
