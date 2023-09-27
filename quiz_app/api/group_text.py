"""
A robust code to converts a large text into groups,
where each group contains a text of no more than 1000 tokens
and a maximum of four PDF pages per group.
This code allows as to also export text in a PDF format.
"""

import fitz  # PyMuPDF library for PDF operations
import re  # Regular expression library


def tokenize_text(text):
    # Tokenize the text into words, punctuation, etc.
    # No tokenization method specified, so I will use regexp. (we shall use a different tokenization method in the feature.)
    tokens = re.findall(r'\w+|[^\w\s]+', text)
    return tokens


def group_text_into_pages(text, max_tokens=1000, max_pages=4):
    tokens = tokenize_text(text)
    curr_page = 0
    curr_tokens = 0
    groups = []
    group_text = ""

    for token in tokens:
        # Calculate the token count and check if it exceeds the maximum
        curr_tokens += 1
        if curr_tokens > max_tokens or curr_page >= max_pages:
            groups.append(group_text)
            group_text = ""
            curr_tokens = 0
            curr_page = 0

        group_text += token + " "

        # Check if the current group exceeds the maximum PDF pages
        if token.endswith((".", "!", "?")):
            curr_page += 1

    # Append the remaining group if any
    if group_text:
        groups.append(group_text)

    return groups


def create_pdf_from_text(text, output_path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text(text)
    doc.save(output_path)
    doc.close()


def convert_to_pdf_groups(text):
    groups = group_text_into_pages(text)

    pdf_groups = []
    for i, group_text in enumerate(groups):
        output_path = f"group_{i+1}.pdf"
        create_pdf_from_text(group_text, output_path)
        pdf_groups.append(output_path)


    return pdf_groups

