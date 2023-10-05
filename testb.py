import os
from dotenv import load_dotenv
from bardapi import Bard

load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")
import requests
'''import requests

def get_bard_response(query):
    bard = Bard(token=BARD_API_KEY)
    prompt = my name is Abdu include my name in your response. our last conversations were [
       me:  hello
       You: Hello! How can I assist you today?
       me: a python function to reverse a list
       You: Certainly! You can use the reverse() method to reverse a list in Python. Here's an example of a Python function that reverses a list:
python
Copy
def reverse_list(lst):
    lst.reverse()
    return lst] based on our previous conversation please answer the following question me: don't use builtin function''
    print(bard.get_answer(prompt))
    
get_bard_response('')
'''


session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", BARD_API_KEY) 
# session.cookies.set("__Secure-1PSID", token) 

bard = Bard(token=BARD_API_KEY, session=session, conversation_id="c_1f04f704a788e6e4", timeout=30)
print(bard.get_answer("is there a better way")['content'])

# Continued conversation without set new session