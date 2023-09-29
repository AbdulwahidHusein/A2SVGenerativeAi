import PyPDF2
from docx import Document
#a class to read files
#supports pdf and docx files
#it returns a text from the file
class FileReader:
    def __init__(self, file) -> None:
        self.file = file
        self.text = ""
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
                return False
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
            return False
            
    def read_file(self, start_page=0, end_page=None):
        try:
            file_name = self.file.name
            file_extension = file_name.split('.')[-1]

            if file_extension == 'pdf':
                return self._read_pdf(start_page, end_page)
            elif file_extension == 'docx':
                return self._read_docx(start_page, end_page)

            return False
        
        except Exception as e:
            print(f"Error reading file: {e}")
            return False