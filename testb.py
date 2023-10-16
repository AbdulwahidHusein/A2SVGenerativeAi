import os
from dotenv import load_dotenv
from bardapi import Bard

load_dotenv()
BARD_API_KEY = os.getenv("BARD_API_KEY")


#bard = Bard(token=BARD_API_KEY, session=session, conversation_id="c_1f04f704a788e6e4", timeout=30)
bard = Bard(token=BARD_API_KEY)
print(bard.get_answer("is there a better way")['content'])

# Continued conversation without set new session