import json
import openai
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_API_KEY")

format = '''
1. Why is cybersecurity important?
A. To prevent financial loss
B. To maintain business continuity
C. To protect sensitive data
D. All of the above
CorrectOption: optionD
Explanation: Cybersecurity is crucial to prevent financial loss, maintain business continuity, and protect sensitive data from unauthorized access. It also helps in preventing reputational damage and legal consequences.
$$$$
2. What does the threat landscape in cyberspace include?
A. Malware
B. Phishing attacks
C. Ransomware
D. All of the above
CorrectOption: optionC
Explanation: The threat landscape in cyberspace is constantly evolving and includes various forms of cyber threats like malware, phishing attacks, ransomware, social engineering, network breaches, and more.
'''

prompt = f'''
 generate a quiz containing 10 multiple choice questions. with the following stric rules
 each questions shoul have a question, four options, correct option and explanation. the quiz must be in the following format """{format}""". notice how A., B., C. and D. are used and coorectOption followed by option + letter. ena explanation + : + explanation. use only the above format an separate each question by four $ signs the is $$$$
 never intrupt a single question text, option or explanation with new line. that is each each question, each options, and each explanation shoul be a single line even if they are so long
 the quiz must look like academic quiz that helps students prepare for exam. use the below text to generate the quiz. note you may only use the the below text to know the relevant topics to generate the quiz.
 The text """
 Cybersecurity is a critical field that focuses on protecting computer systems, networks, and data from unauthorized access, theft, damage, or disruption. It encompasses various measures, practices, technologies, and policies designed to defend against cyber threats and ensure the confidentiality, integrity, and availability of information.

Here are a few important points to note about cybersecurity:

Importance of Cybersecurity: With the increasing reliance on technology and interconnected systems, the potential risks and impact of cyber threats have also grown. Cybersecurity is crucial to safeguard sensitive data, prevent unauthorized access, maintain business continuity, and protect individuals and organizations from financial loss, reputational damage, and legal consequences.

Threat Landscape: The threat landscape in cyberspace is constantly evolving. Cyber threats can come in various forms, including malware, phishing attacks, ransomware, social engineering, network breaches, and more. Attackers are often motivated by financial gain, espionage, activism, or disruption.

Security Measures: Cybersecurity involves implementing a range of security measures to mitigate risks. This includes network security, endpoint protection, encryption, access controls, intrusion detection and prevention systems, secure coding practices, regular software updates, employee training, and incident response planning.

Risk Management: It's important to adopt a risk-based approach to cybersecurity. Organizations should assess their assets, identify vulnerabilities and potential threats, and prioritize their security efforts based on the potential impact and likelihood of occurrence. Implementing a comprehensive cybersecurity framework, such as the NIST Cybersecurity
 """
'''
def chat(history):
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages = history,
        )
        generated_response = completion.choices[0].message["content"]
        return generated_response


messages = [
        {"role": "system", "content": "You are A Quiz Generator that generates a quiz in a format the  user requested. and helps students prepare for their exam"},
        {"role": "user", "content": "are you ready"},
        {"role": "assistant", "content": "sure i am. i will generate a qui as you specified"},
        {"role": "user", "content": prompt}
    ]
generated_message = chat(messages)

print(generated_message)















quiz_text = """
sure here is 10 questions
[
1. What is D
jango?
A. A programming language
B. A web framework
C. A database management system
D. A version control system
CorrectOption: Option B
Explanation: Django is a web framework written in Python that simplifies the process of building web applications.

$$$$$$$$$$

2. What is the purpose of Django's ORM (Object-Relational Mapping)? fdgdf
A. To provide a graphical 
user interface for Django projects
B. To handle URL routing 
in Django applications
C. To interact with the database using Python objects
D. To manage the authentication and authorization in Django
CorrectOption: Option C
Explanation: Django's ORM allows developers to interact with the database using Python code instead of writing raw SQL queries.
This is a multiline explanation.
It can span multiple lines.
]
...

"""
import re

match = re.search(r'\[(.+)\]', quiz_text, re.DOTALL)
if match:
    if match:
            quiz_text = match.group(1)
def replace_new_lines(text):
    pattern =  r"\n(?! *([ABCD]\.|Corr|Exp))"
    replaced_text = re.sub(pattern, " ", text)
    return replaced_text

questions = quiz_text.strip().split("$$$$$$$$$$")
quiz_data = []

for question in questions:
    question = replace_new_lines(question)
    lines = question.strip().split("\n")
    q_text = lines[0].split(".")[1]
    
    options = []
    correct_option = ""
    explanation = question[question.index("Explanation:")+1:]


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
        "Explanation": explanation
    }

    quiz_data.append(question_data)

quiz_json = json.dumps(quiz_data)
print(quiz_json)
#print(quiz_json)
