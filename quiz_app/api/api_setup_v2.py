import openai


class PromptGenerator:
    
    def __init__(self, text_data, difficulty):
        self.text = text_data
        self.difficulty_sentences = ''

        self.difficulty = difficulty
        if difficulty == 'easy':
            self.difficulty_sentences = 'the generated questions should be easy so that elementart students can answer'
        elif difficulty == 'medium':
            self.difficulty_sentences = 'the generated questions should have medium difficulty so that avarage persons can answer them'
        else:
            self.difficulty_sentences = 'the generated questions should be so hard that only person who deeply understand the topic can answer any of the questions'
            
    def make_multiple_choice_prompt(self, number_of_questions, question_format):
        prompt = f'''You are helpful Quiz generator
            Please generate a quiz containing {number_of_questions} multiple-choice questions. {self.difficulty_sentences}. The quiz should follow the strict rules below:
    - the quiz must be enclosed in square brackets [ ].
    - Each question should consist of a question, four options, the correct option, and an explanation Note The quiz should contain {number_of_questions} questions!!.
    - The quiz should be generated in the following format or demo but the number of questions you generate is {number_of_questions} here is the format : """" {question_format}"""". Note the use of A., B., C., and D., and the placement of the correct option followed by the option letter.
    - The quiz should be enclosed in square brackets [ ], and each question should be separated by four dollar signs $$$$ as indicated in the format. Ensure that the text, options, and explanations for each question are on a single line, even if they are long.
    - The quiz should resemble an academic quiz that helps students prepare for an exam.

    the following keywords are extracted from the book from which the quiz is to be generated. therefore generate the quiz that is related 
    to these topics and their relationships
    """"{self.text}""""
    Thank You for your assistance and for understanding my context!
    '''
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
    
    def generate_question(self, prompt):
        prompt_token_length = len([w for w in prompt.split()])
        max_tokens = 3100 - prompt_token_length 
        parameters = {
            'model': 'text-davinci-003',  
            
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': 0.7,  # Adjust the temperature to control the randomness of the output
            'n': 1,  # Generate a single reply
            'stop': None,  # You can specify a stop sequence to control the length of the completion
        }
        response = openai.Completion.create(**parameters)
        reply = response.choices[0].text.strip()
        return reply
        
