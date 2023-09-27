import openai
from bardapi import Bard


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
        response = openai.Completion.create(**parameters)
        reply = response.choices[0].text.strip()
        return reply
        
    
class BardEx:
    def __init__(self, API_KEY, session, conversation_id) -> None:
        self.api_key = API_KEY
        self.conversation_id = conversation_id
        self.session = session
        self.bard = Bard(API_KEY=self.api_key, session=self.session, conversation_id=self.conversation_id)
        
    def get_answer(self, question):
        answer = self.bard.get_answer(question)
        return answer['content']
