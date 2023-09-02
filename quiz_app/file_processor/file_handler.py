import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from docx import Document

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
    
    def read_docx(self, start_page = 0, end_page = 0 ):
        document = Document(self.file)
        paragraphs = document.paragraphs
        num_pages = len(paragraphs)
        if end_page == 0:
            end_page = num_pages - 1
        if end_page >= num_pages:
            end_page = num_pages - 1
        extracted_paragraphs = paragraphs[start_page:end_page+1]
        extracted_text = [paragraph.text for paragraph in extracted_paragraphs]
        final = " ".join(extracted_text)
        self.text = final.strip()
        return final.strip()
    
    def summerized(self):
        parser = PlaintextParser.from_string(self.text, Tokenizer("english"))
        summary = self.summerizer(parser.document, len(self.text)/10)
        summ = ""
        for word in summary:
                summ += str(word)
        return summ



file = FileHandler("/home/samuel/Desktop/SamuelLegesseLAB3.docx")
print(file.read_docx(0, 5))
print("\n\nsummerized\n")
print(file.summerized())
