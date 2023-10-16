import sys
sys.path.append("..") 
from quiz_app.api import api_caller
from quiz_app.file_processor import file_reader, file_summerizer, file_chunk

def read_summerize_split(file, start_page, end_page):
    '''read and summerise'''
    reader = file_reader.FileReader(file)
    if end_page - start_page > 10:
        end_page = start_page + 10
        
    file_content = reader.read_file(start_page, end_page) 
    splitted = []
    divider = 2
    if file_content:
        summerizer =  file_summerizer.Summerizer(file_content)
        summerized = summerizer.summarize(divider)#1/3 of the original number of sentence
        splitted = file_chunk.split_text_into_groups(summerized, 100, 500)
        
        while len(splitted) > 5:
            summerizer =  file_summerizer.Summerizer(' '.join(splitted))
            summerized = summerizer.summarize(divider)#1/3 of the original number of sentence
            splitted = file_chunk.split_text_into_groups(summerized, 100, 500)
            
        return splitted
    else:
        return False
    
    '''make a prompt'''
    
    
def get_question(file, num_of_questions, difficulty, start_page, end_page, mode, model):
    #mode can be multiple_choice or short_answer
    summerized_data = read_summerize_split(file, start_page, end_page)
    
    response = {}
    question_generator = api_caller.GenerateQuestionRequest(summerized_data[0], model)
    questions = question_generator.make_request(num_of_questions, difficulty, mode)
    
    return questions


if __name__ == '__main__':
    with open("c:\\Users\\Abdi\\Desktop\\A2SVGenerativeAi\\quiz_app/drf.pdf", 'rb') as df:
        q = get_question(df, 5, 'hard', 30, 50, 'multiple_choice', 'chatgpt')
        print(q)
        '''f = read_summerize_split(df, 10,  100)
        print(f)
        print('\n\n\n\n\n\n')
        print(len(f))'''