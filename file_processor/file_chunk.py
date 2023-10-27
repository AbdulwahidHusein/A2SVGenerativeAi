import re


#given a text data it returns array of texts each having lessthan or equal to X tokens
def split_text_into_groups(text, max_group_count, max_token_per_group):
        tokens = re.findall(r'\w+|[^\w\s]+', text)
        groups = []
        current_group = []
        token_count = 0

        for token in tokens:
            current_group.append(token)
            token_count += 1

            if token_count >= max_token_per_group:
                groups.append(' '.join(current_group))
                current_group = []
                token_count = 0

            if len(groups) >= max_group_count:
                break

        if current_group:
            groups.append(' '.join(current_group))

        return groups


#
'''class FileChunker:
    def __init__(self, text_data) -> None:
        self.text_data = text_data
        self.chunked_text_aray = []
        
    def chunk_text(self, length_per_chunk):
            try:
                assert length_per_chunk > 0

                total_length = len(self.text_data)
                start = 0
                end = length_per_chunk

                while end < total_length:
                    last_char = self.text_data[end]
                    while last_char != '.' and end < total_length:
                        end += 1
                        last_char = self.text_data[end]

                    self.chunked_text_aray.append(self.text_data[start:end + 1])
                    start = end + 1
                    end += length_per_chunk

                return self.chunked_text_aray
            except Exception as e:
                print(f"Error chunking text: {e}")
                return []
'''






if __name__ == '__main__':
        
    ttt = '''
    The provided code is a Python script that performs several operations on a large text:

    Tokenization: The tokenize_text function takes a text as input and tokenizes it into words, punctuation, etc. It uses regular expressions (re.findall) to identify word and non-word tokens.

    Grouping Text: The group_text_into_pages function takes a text, maximum number of tokens (max_tokens), and maximum number of pages (max_pages) as inputs. It uses the tokenize_text function to tokenize the text. Then, it iterates over the tokens and groups them into chunks of text, where each group contains no more than max_tokens tokens and a maximum of max_pages PDF pages. The groups are split based on punctuation marks (such as ".", "!", "?"), and a new group is started whenever the token count or page count exceeds the specified limits.

    Creating PDFs: The create_pdf_from_text function takes a text and an output path as inputs. It uses the PyMuPDF library (fitz) to create a new PDF document, insert the text into a new page, and save the PDF to the specified output path.

    Conversion to PDF Groups: The convert_to_pdf_groups function takes a text as input. It calls the group_text_into_pages function to obtain the text groups. Then, it iterates over the groups, creates a PDF for each group using the create_pdf_from_text function, and stores the output paths of the PDFs in a list.

    The code provides a way to break down a large text into manageable groups based on token count and PDF page count. It also allows for the conversion of each group into a separate PDF file.

    Note: The code assumes the presence of the PyMuPDF library (fitz) and the regular expression library (re) to be installed in the environment where the code is executed.
    The provided code is a Python script that performs several operations on a large text:

    Tokenization: The tokenize_text function takes a text as input and tokenizes it into words, punctuation, etc. It uses regular expressions (re.findall) to identify word and non-word tokens.

    Grouping Text: The group_text_into_pages function takes a text, maximum number of tokens (max_tokens), and maximum number of pages (max_pages) as inputs. It uses the tokenize_text function to tokenize the text. Then, it iterates over the tokens and groups them into chunks of text, where each group contains no more than max_tokens tokens and a maximum of max_pages PDF pages. The groups are split based on punctuation marks (such as ".", "!", "?"), and a new group is started whenever the token count or page count exceeds the specified limits.

    Creating PDFs: The create_pdf_from_text function takes a text and an output path as inputs. It uses the PyMuPDF library (fitz) to create a new PDF document, insert the text into a new page, and save the PDF to the specified output path.

    Conversion to PDF Groups: The convert_to_pdf_groups function takes a text as input. It calls the group_text_into_pages function to obtain the text groups. Then, it iterates over the groups, creates a PDF for each group using the create_pdf_from_text function, and stores the output paths of the PDFs in a list.

    The code provides a way to break down a large text into manageable groups based on token count and PDF page count. It also allows for the conversion of each group into a separate PDF file.

    Note: The code assumes the presence of the PyMuPDF library (fitz) and the regular expression library (re) to be installed in the environment where the code is executed.
    The provided code is a Python script that performs several operations on a large text:

    Tokenization: The tokenize_text function takes a text as input and tokenizes it into words, punctuation, etc. It uses regular expressions (re.findall) to identify word and non-word tokens.

    Grouping Text: The group_text_into_pages function takes a text, maximum number of tokens (max_tokens), and maximum number of pages (max_pages) as inputs. It uses the tokenize_text function to tokenize the text. Then, it iterates over the tokens and groups them into chunks of text, where each group contains no more than max_tokens tokens and a maximum of max_pages PDF pages. The groups are split based on punctuation marks (such as ".", "!", "?"), and a new group is started whenever the token count or page count exceeds the specified limits.

    Creating PDFs: The create_pdf_from_text function takes a text and an output path as inputs. It uses the PyMuPDF library (fitz) to create a new PDF document, insert the text into a new page, and save the PDF to the specified output path.

    Conversion to PDF Groups: The convert_to_pdf_groups function takes a text as input. It calls the group_text_into_pages function to obtain the text groups. Then, it iterates over the groups, creates a PDF for each group using the create_pdf_from_text function, and stores the output paths of the PDFs in a list.

    The code provides a way to break down a large text into manageable groups based on token count and PDF page count. It also allows for the conversion of each group into a separate PDF file.

    Note: The code assumes the presence of the PyMuPDF library (fitz) and the regular expression library (re) to be installed in the environment where the code is executed.
    The provided code is a Python script that performs several operations on a large text:

    Tokenization: The tokenize_text function takes a text as input and tokenizes it into words, punctuation, etc. It uses regular expressions (re.findall) to identify word and non-word tokens.

    Grouping Text: The group_text_into_pages function takes a text, maximum number of tokens (max_tokens), and maximum number of pages (max_pages) as inputs. It uses the tokenize_text function to tokenize the text. Then, it iterates over the tokens and groups them into chunks of text, where each group contains no more than max_tokens tokens and a maximum of max_pages PDF pages. The groups are split based on punctuation marks (such as ".", "!", "?"), and a new group is started whenever the token count or page count exceeds the specified limits.

    Creating PDFs: The create_pdf_from_text function takes a text and an output path as inputs. It uses the PyMuPDF library (fitz) to create a new PDF document, insert the text into a new page, and save the PDF to the specified output path.

    Conversion to PDF Groups: The convert_to_pdf_groups function takes a text as input. It calls the group_text_into_pages function to obtain the text groups. Then, it iterates over the groups, creates a PDF for each group using the create_pdf_from_text function, and stores the output paths of the PDFs in a list.

    The code provides a way to break down a large text into manageable groups based on token count and PDF page count. It also allows for the conversion of each group into a separate PDF file.

    Note: The code assumes the presence of the PyMuPDF library (fitz) and the regular expression library (re) to be installed in the environment where the code is executed.

    '''

    for l in split_text_into_groups(ttt, 13, 1000):
        print(l)
        print('\n\n\n')