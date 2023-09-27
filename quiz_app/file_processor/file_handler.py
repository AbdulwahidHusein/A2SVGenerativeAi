import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from docx import Document
from stop_words import get_stop_words


class FileHandler:
    def __init__(self, file):
        self.file = file
        self.text = ""
        self.summarizer = LexRankSummarizer()
        self.summarized_data = ""

    def _read_pdf(self, start_page=0, end_page=None):
        try:
            pdf_reader = PyPDF2.PdfReader(self.file)
            num_pages = len(pdf_reader.pages)

            if end_page is None:
                end_page = num_pages
            if end_page >= num_pages:
                end_page = num_pages - 1

            for page in range(start_page, end_page + 1):
                self.text += pdf_reader.pages[page].extract_text().strip()
            return self.text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""

    def _read_docx(self, start_page=0, end_page=None):
        try:
            document = Document(self.file)
            paragraphs = document.paragraphs
            num_pages = len(paragraphs)
            if end_page is None:
                end_page = num_pages - 1
            if end_page >= num_pages:
                end_page = num_pages - 1
            extracted_paragraphs = paragraphs[start_page:end_page + 1]
            extracted_text = [paragraph.text for paragraph in extracted_paragraphs]
            final = " ".join(extracted_text)
            self.text = final.strip()
            return final.strip()
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""

    def remove_stop_words(self):
        try:
            stop_words = get_stop_words('english')
            tokens = self.summarized_data.split()
            filtered_text = [word for word in tokens if word.casefold() not in stop_words]
            self.summarized_data = ' '.join(filtered_text)
            return self.summarized_data
        except Exception as e:
            print(f"Error removing stop words: {e}")
            return ""

    def chunked_text(self, length_per_chunk):
        try:
            assert length_per_chunk > 0

            total_length = len(self.summarized_data)
            start = 0
            end = length_per_chunk
            chunked_texts = []

            while end < total_length:
                last_char = self.summarized_data[end]
                while last_char != '.' and end < total_length:
                    end += 1
                    last_char = self.summarized_data[end]

                chunked_texts.append(self.summarized_data[start:end + 1])
                start = end + 1
                end += length_per_chunk

            return chunked_texts
        except Exception as e:
            print(f"Error chunking text: {e}")
            return []

    def summarized(self, divider):
        try:
            assert divider >= 1

            length_of_sentences = len([sentence for sentence in self.text.split('.')])

            parser = PlaintextParser.from_string(self.text, Tokenizer("english"))
            summary = self.summarizer(parser.document, length_of_sentences // divider)

            data = "".join(str(word) for word in summary)
            self.summarized_data = data

            return data
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return ""

    def read_file(self, start_page=0, end_page=None):
        try:
            file_name = self.file.name
            file_extension = file_name.split('.')[-1]

            if file_extension == 'pdf':
                return self._read_pdf(start_page, end_page)
            elif file_extension == 'docx':
                return self._read_docx(start_page, end_page)

            return ""
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""


'''
Usage:

file = open('example.pdf', 'rb')
file_handler = FileHandler(file)

# Read the file
text = file_handler.read_file(start_page=0, end_page=3)
# Remove stop words

summary_without_stop_words = file_handler.remove_stop_words()

# Summarize the text
summary = file_handler.summarized(divider=2)



# Chunk the text
chunked_text = file_handler.chunked_text(length_per_chunk=500)
'''