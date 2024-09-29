from pprint import pprint
from nltk import tokenize
from PyPDF2 import PdfReader
from summarizer.algorithms.scoring import scoring_algorithm
from summarizer.algorithms.scoring.util import clean_text, summarize_text

def summarize_pdf(pdf_file, sent_percentage):
    # Open the PDF file
    with open(pdf_file, 'rb') as pdf_file_obj:
        pdf_reader = PdfReader(pdf_file_obj)
        title = pdf_reader.metadata.title
        summary_title = "Summary"
        if title is not None:
            summary_title = title + ' - ' + summary_title
        
        num_of_pages = len(pdf_reader.pages)
        body = ''
        for i in range(num_of_pages):
            page = pdf_reader.pages[i]
            body += "\n\n" + page.extract_text()

    # Process the extracted text
    body = clean_text(body)
    sentences = count_sent(body)
    sentence_no = int((sent_percentage / 100) * sentences)

    print(sentences)
    print(sentence_no)
    print('-------------------')

    result_list = summarize_text(body, sentence_no)
    summary = "\r\n".join(result_list)  # \r only for display in notepad but \n is valid for end-of-line
    summary = summary_title + "\r\n\r\n" + summary

    return summary

def count_sent(pdf_body):
    count = 0
    pags = pdf_body.split('\n\n')
    for p in pags:
        count = count + len(tokenize.sent_tokenize(p))

    return count
