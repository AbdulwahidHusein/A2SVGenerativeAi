import re
import regex
import json

def replace_newlines(text):
    text = re.sub(r"(\b\w+)\"(\w+\b)", r"\1 \2", text)# substitute dont"t by don t
    text = re.sub(r'\n', ' ', text)#remove any new line
    text = re.sub(r'(\"(?:\s*)\")', '", "', text)#add comma beetween key value pairs if forgotten
    
    #remove all unecesary double quotes
    pattern = r'(?<=[\[{]|:|,)\s*\"|\"\s*(?=[\]}]|,)'
    #text =  re.sub(pattern, lambda m: m.group(0) if any([m.group(0).startswith(x) for x in ['[', '{', ':', ',', '}', ']']]) else '', text)
    print(text)
    
    
    #text = regex.sub(r'(?<!: *)"(?!,|\n *\})(?<!\b")', " ", text)
    '''replaces any double quote if it doesnt satisfy one of the following conditions. 1, if not preceded by colon + zero or some number of empty spaces. 2, not followed by comma. 3 not followed by new line + some some number of empty space + closing curly brace'''
    print(text)
    #pattern = r"(?<!,)(?<![{}<>])\n(?!\s*})"#remove new innapropirate lines 
    
    replacement = " "
    #processed_text = re.sub(pattern, replacement, text)
    return text

# Example usage
input_text = '''{
    
  "questions": [
    {
      "question": "What is the Loebner Prize?" 
      "answer": "The Loebner Prize is an annual ,'
      competition in artificial intell
      igence that awards prizes to the computer programs considered by the judges to be the most human-like, using the Turing Test computer and person arrangement."
    },
     {
      "question" : "What is the Loebner Prize?" 
      "answer": "The Loebner Prize is an annual ,'
      competition in artificial intell
      igence that awards prizes lk"to the computer programs considered by the judges to be the most human-like, using the Turing Test computer and person arrangement."
    },
     {
      "question" : "What is the Loebner Prize?" 
      "answecr": "The Loebner Prize is an annual"
      "answer": "The Loebner Prize is an annual ,'
      competition in artificial intell
      igence that awards prizes to the computer programs considered by the judges to be the most human-like, using the Turing Test computer and person arrangement."
    }
  ]
}
'''

processed_text =  replace_newlines(input_text)
print(json.loads(processed_text))

