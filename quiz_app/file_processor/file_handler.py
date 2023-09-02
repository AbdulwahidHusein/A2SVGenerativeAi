import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

class FileHandler:
    def __init__(self, file) -> None:
        self.file = file
        self.text = ""
        self.summerizer = LexRankSummarizer()
        self.summerised_data = ""


    def read_pdf(self, start_page = 0, end_page = 0):
        pdf_reader = PyPDF2.PdfReader(self.file)
        num_pages = len(pdf_reader.pages)

        if end_page == 0:
            end_page = num_pages
        if end_page >= num_pages:
            end_page = num_pages - 1

        for page in range(start_page, end_page + 1):
            self.text += pdf_reader.pages[page].extract_text().strip()
        return self.text
    

    def summerized(self, num_tokens):
        stop_words = [',','.','!', '?', ';', '<', '>', '@', '#', '$', '\\']
        parser = PlaintextParser.from_string(self.text, Tokenizer("english"))
        summary = self.summerizer(parser.document, sentences_count=num_tokens)
        count = 0
        text = ''
        for i in summary:
            for j in str(i):
                if count >= num_tokens:
                    return ((text))
                if j not in stop_words:
                    text += j
                    count += 1
                    


