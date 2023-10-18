import json
import re
# import openai
# from dotenv import load_dotenv
# import os
# load_dotenv()
# openai.api_key = os.getenv("OPEN_AI_API_KEY")

# format = '''
# [
# 1. Why is cybersecurity important?
# A. To prevent financial loss
# B. To maintain business continuity
# C. To protect sensitive data
# D. All of the above

class ResponseParser:
    def __init__(self, generated_messsage) -> None:
        self.generated_message = generated_messsage
        
    def replace_new_lines(self, text):
        pattern =  r"\n(?! *([ABCD]\.|Corr|Exp))"
        replaced_text = re.sub(pattern, r" ", text)
        replaced_text = re.sub(r'"', r" ", replaced_text)
        replaced_text = re.sub(r"'", r' ', replaced_text)
        return replaced_text
        
    def _parse_multiple_choice(self):
        match = re.search(r'\[(.+)\]', self.generated_message, re.DOTALL)

        if match:
            self.generated_message = match.group(1)
        else:
            self.generated_message = self.generated_message[self.generated_message.index('[')+1:]
        if True:
            questions = self.generated_message.strip().split("$$$$")
            
            quiz_data = []
            for question in questions:
                question = self.replace_new_lines(question)
                lines = question.strip().split("\n")
                q_text = lines[0].split(".")[1]
                
                options = []
                correct_option = ""
                explanation = question[question.index("Explanation:")+12:]


                # Combine multiline options
                option = ""
                for line in lines[1:]:
                    line.strip()
                    if line.startswith(("A.", "B.", "C.", "D.")) or line.startswith(("A)", "B)", "C)", "D)")) or line.startswith(("a.", "b.", "c.", "d.")) or line.startswith(("a)", "b)", "c)", "d)")):
                        option = line[line.index(".") + 1:].strip()
                        options.append(option)
                        
                    elif line.startswith("CorrectOption"):
                        correct_option = line[14:].strip()



                question_data = {
                    "question": q_text.strip(),
                    "optionA": options[0],
                    "optionB": options[1],
                    "optionC": options[2],
                    "optionD": options[3],
                    "correctOption": correct_option,
                    "explanation": explanation
                }

                quiz_data.append(question_data)
            return quiz_data
    def get_json_data(self):
        supported_format = {}
        data =  self._parse_multiple_choice()
        supported_format['questions'] = data
        
        return supported_format
        