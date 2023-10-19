import sys
sys.path.append("..") 
from quiz_app.api import api_caller_v2
from quiz_app.file_processor import file_reader, file_summerizer, file_chunk, keyword_extractor

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
        #this should be error
        return ["file not found"]
    
    '''make a prompt'''
#another alternative
def red_extract_keyword(file, start_page, end_page):
    end_page = min(start_page+30, end_page)
    reader = file_reader.FileReader(file)
    file_content = reader.read_file(start_page, end_page) 
    if file_content:
        keywwords = keyword_extractor.extract_keywords(file_content,(end_page-start_page)*10)
        return keywwords
    raise Exception("error reading a file")
    
def get_question(file, num_of_questions, difficulty, start_page, end_page, mode, model):
    num_of_questions = max(int(num_of_questions), 10)#for now only support <= 10 questions
    #mode can be multiple_choice or short_answer
    #summerized_data = read_summerize_split(file, start_page, end_page)
    keywords = red_extract_keyword(file, start_page, end_page)#for now we use kewords instead
    summerized_data = keywords
    if summerized_data:
        print(summerized_data)
        #use v2
        question_generator = api_caller_v2.GenerateQuestionRequest(summerized_data, model)
        questions = question_generator.make_request(num_of_questions, difficulty, mode)
        
        return questions
    else:
        #this should be handled in views.py
        return False


if __name__ == '__main__':
    with open("c:\\Users\\Abdi\\Desktop\\A2SVGenerativeAi\\quiz_app/drf.pdf", 'rb') as df:
        q = get_question(df, 5, 'hard', 30, 50, 'multiple_choice', 'chatgpt')
        print(q)
        '''f = read_summerize_split(df, 10,  100)
        print(f)
        print('\n\n\n\n\n\n')
        print(len(f))'''