##pip install gensim==3.8.3

import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import gensim
from gensim.summarization import summarize
from gensim.summarization.textcleaner import split_sentences


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
        sentences = split_sentences(self.text)

        # Join sentences until the desired number of tokens is reached
        summary = ''
        tokens_count = 0
        for sentence in sentences:
            summary += sentence + ' '
            tokens_count = len(summary.split())
            if tokens_count >= num_tokens:
                break

        # Use Gensim's summarize function iteratively to refine the summary
        while tokens_count > num_tokens:
            summary = summarize(summary, ratio=num_tokens / tokens_count, split=True)
            summary = ' '.join(summary)
            tokens_count = len(summary.split())

        return summary.strip()

test = FileHandler("/home/samuel/Desktop/2nd_year/2nd_semester/Database/Raghu_Ramakrishnan_Database_Management_Systems_Ramakrishnan_2018.pdf")
print((len(test.read_pdf(25, 35))))
print('\n Summerization\n \n')
print(len(test.summerized(1000)))



