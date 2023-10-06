import re
import json

class ResponseParser:
    
    def __init__(self, text, mode) -> None:
        self.text = text
        self.json_data = {}
        self.mode = mode
        print(text)

    def _extract_json_text(self):
        # Extract the JSON object from the response text
        match = re.search(r'{(.+)}', self.text, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            raise ValueError("Invalid response text. JSON object not found.")
        #replace any single quote by double quote
        json_text = '{'+json_text+'}'
        self.text = json_text
        
        return json_text
    
    def _make_improvements(self):
        json_text = re.sub(r"'", '"', self.text)
        #ensure there is quote after colon
        json_text = re.sub(r":(?!(\[| \[|\"| \"|\]))", ':"', json_text)
        #replace any newline by space
        
        #replace words like don't and didn't by like dont and didnt 
        json_text = re.sub(r"(\b\w+)\"(\w+\b)", r"\1 \2", json_text)
        #json_text = re.sub(r'"(?:\s*,\s*|\s*,\s*)\n', ' ', json_text)
        
        #replace all new lines thet intrupts the string 
        #json_text = re.sub(r"\n(?!question|optionA|optionB|optionC|optionD|correctOption|explanation|\})", ' ', json_text)
        #add comma before newline 
        json_text = re.sub(r"(?<!,|\]|\{|\[)(?<!\n)(?!\s*(question|optionA|optionB|optionC|optionD|correctOption|explanation|\{|\[|\}|\]))\n", ',\n', json_text)# Convert the JSON object to a Python dictionary
        self.text = json_text
        
        return self.text
    
    def _check_multiple_choice_formating(self):
        for question in self.json_data['questions']:
            if 'correctOption' in question and len(question['correctOption'].strip()) == 1:
                letter = question['correctOption']
                letter = letter.strip()
                option_key = 'option' + letter.upper()
                if option_key in question:
                    question['correctOption'] = option_key
        
    def _process_json_text(self):
        try:
            self.json_data = json.loads(self.text)
            self._check_multiple_choice_formating()
            return self.json_data
        except:
            self._make_improvements()
            print(self.text)
            try:
                self.json_data = json.loads(self.text)
                self._check_multiple_choice_formating()
                return self.json_data
            except:
                raise Exception("the geven text can not be parsed in to json format")
            
    def get_json_data(self):
        if self.mode == 'multiple_choice':
            self._extract_json_text()
            self._process_json_text()
        
        elif self.mode == 'short_answer':
            self._extract_json_text()
            self._process_json_text()


        return self.json_data