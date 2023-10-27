import openai
from bardapi import Bard

class PromptGenerator:
    
    def __init__(self, text_data, difficulty):
        self.text = text_data
        self.difficulty_sentences = ''
        self.prompt = ""
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.difficulty_sentence = 'the generated questions should be easy so that elementart students can answer'
        elif difficulty == 'medium':
            self.difficulty_sentences = 'the generated questions should have medium difficulty so that avarage persons can answer them'
        else:
            self.difficulty_sentences = 'the generated questions should be so hard that only person who deeply understand the topic can answer any of the questions'
            
    def make_multiple_choice_prompt(self, number_of_questions, question_format):
        
        prompt  = f'''You are helpful Quiz generator
            Please generate a quiz that consists of {number_of_questions} different multiple-choice questions.{self.difficulty_sentences} Each question should have a unique context and four choices. The questions must be returned in the following format: {question_format}. 
            Please note that each question and explanation should not be more than two lines and explanations should not repeat the correct choice. It is important to ensure that all items are quoted to avoid JSON errors. Do not use quoted words that may interfere with the string's quotation. Remember to quote each item properly.
            NEVER INSERT NEW LINES WITHIN A SINGLE ITEM THAT ITEM MAY BE Question, CHOICE, OR EXPLANATION The question itself should be a valid JSON format with appropriate quotes and commas. The correct option should be written as "option" followed by the option letter, e.g., optionA.
            Please use the provided text to generate the quiz THE TEXT: {self.text}, along with this note Please Enusre to respond in correct format I give above other wise it raises a great error.
            Sincerely,
            '''
        self.prompt = prompt
        return prompt
    
    def make_short_answer_propmt(self, number_of_questions, question_format):
        prompt  = f'''Dear AI Model,
            Please generate a quiz that consists of {number_of_questions} different short answer questions.{self.difficulty_sentences} Each question should have a unique context. Set the difficulty level to {self.difficulty_sentences}. The questions must be returned in the following format: {question_format}. 

            Please note that each question should not be more than two lines NEVER INSERT NEW LINES WITHIN A SINGLE ITEM THAT ITEM MAY BE A QUESTION OR ANSWER. It is important to ensure that all items are quoted to avoid JSON errors. Do not use quoted words that may interfere with the string's quotation. Remember to quote each item properly.

            The question itself should be a valid JSON format with appropriate quotes and commas. 
            Please use the provided text to generate the quiz THE TEXT: {self.text}, along with this note. Enusre to respond in correct format I give above other wise it raises a great error.

            Thank you for your assistance in generating the quiz.

            Sincerely,
            '''
        self.prompt = prompt
        return prompt
        

class OpenAi:

    def __init__(self, API_KEY):
        
        self.api_key = API_KEY
        openai.api_key = self.api_key
        
    def chat(self, history, query, user):
        conversation_history = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        for chat in history:
            if chat.is_received:
                hist = {'role':'assistant', 'content':chat.text}
                conversation_history.append(hist)
            else:
                hist = {'role':'user', 'content':chat.text}
                conversation_history.append(hist)
        conversation_history.append({'role':'user','content':"assume you are an assistant in quiz website called Quizme in which AI like you generates an interactive quiz from their study material and users ask more calarification about these questions. now you are assisting a person named "+user.first_name + "be freindly with them"})
        conversation_history.append({'role':'user','content':query})
        
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages = conversation_history,
        )
        generated_response = completion.choices[0].message["content"]
        return generated_response
    
    def generate_question(self, prompt):
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
    def gudge_short_answer_submission(self, submission):
        feedback_format = """
        [
            what is 1+1?
            1+1 is 2
            you are correct 1+1 is 2. this is a simple mathematical concept ...
            $$$$
            what is the big bang?
            it is a big thing
            your answer for this question is wrong or incomplete. in theoretical physics the big bang is an event that happend billons of years ago ans it is believed to be the cause for the birth od the universe
            $$$$
            what is motion?
            moion is the movement of particles
            your answer for this question seems correct but it is not accurate. you need to improve your explanation. motion is the change of spac coordinate of an object through the passage of time
            ]
            """
        prompt = f"""
        You are helpful quiz judge.
        JUDGE THE FOLLOWING QUIZ OBJECTIVELY 
        the following question answer pairs was submitted by me '''{submission}''' Judge these submissions
        when the key of the above object is the question the value is the my answer for that question
        so based on that judge the my answers wheather they are right or wrong and give me corrective feedback and challange my answers for each question.
        your response should be in the following format '''{feedback_format}''' 
        NOTE the above feedback format is only a demo templete give your feedback for my quiz i provided erlier
        NOTICE YOU CAN ONLY RETURN YOUR RESPONSE IN THE GIVEN FORMAT ABOVE: WHERE
        THE FEEDBACK MUST BE ENCLOSED WITH ANGLE BRACKETS [ ] AND FEEDBACK FOR EACH QUESTION IS SEPARATED BY NEW LINE + FOUR DOLLAR SIGHNS I.E $$$$ AND A NEW LINE
        FOR EACH QUESTION THE FEEDBACK ONLY CONTAINS THREE LINES THE FIRST LINE IS THE ORIGINAL QUESTION THE SECOND LINE IS MY ANSWER WITH OUT ANY MODIFICATION AND
        THE THIRD LINE IS YOUR FEEDBACK FOR MY ANSWER IN ADDITION TO FURTHER EXPLANATION
        AND NEVER USE QUOTED WORDS SINCE I WANT TO PARSE THAT TEXT TO JSON. EACH QUESTION MY ANSWER AND YOU FEED BACK SHOUL NOT CONTAIN NEW LINE THEY MUST BE IN A SINGLE LINE
        FOR EACH QUESTION THE FEEDBACK MUST BE THREE LINE AND EACH FEEDBACKS MUST BESEPARATED BY NEW LINE + $$$$ + LEWLINE
        AND YOU MUST OBJECTIVELY JUDGE MY QUIZ. MAKE YOU EXPLANTIONS DETAILED. Do not forget to enclose your response with [ ]
        there must be [ at the start of your response and ] at the end as included in the demo
        
        THANK YOU FOR YOUR ASSISTANCE
        """
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
        

 
class BardEx:
    def __init__(self, API_KEY) -> None:
        self.api_key = API_KEY
        self.bard = Bard(token=self.api_key)
        
    def get_answer(self, question):
        answer = self.bard.get_answer(question)
        return answer['content']
