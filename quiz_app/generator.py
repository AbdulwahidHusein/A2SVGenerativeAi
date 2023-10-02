
from quiz_app.api import api_caller
from quiz_app.file_processor import file_reader, file_summerizer, file_chunk
from .models import Quiz

def read_summerize_split(file, spage, epage):
    '''read and summerise'''
    reader = file_reader.FileReader(file)
    file_content = reader.read_file(spage, epage)
    splitted = []
    divider = 2
    if file_content:
        summerizer =  file_summerizer.Summerizer(file_content)
        summerized = summerizer.summarize(divider)#1/3 of the original number of sentence
        splitted = file_chunk.split_text_into_groups(summerized, 100, 1000)
        
        while len(splitted) > 3:
            divider += 1
            summerized = summerizer.summarize(divider)#1/3 of the original number of sentence
            splitted = file_chunk.split_text_into_groups(summerized, 100, 1000)
            
        return splitted
    else:
        return False
    
    '''make a prompt'''
    
    
def get_question(file, num_of_questions, difficulty, spage, epage):
    
    summerized_data = read_summerize_split(file, spage, epage)
    
    response = {}
    question_generator = api_caller.GenerateQuestionRequest(summerized_data[0], 'chatgpt') 
    questions = question_generator.make_request(num_of_questions, difficulty)
        
        
        
        
    