"""
Utility functions for filtering content
"""
import re
from nltk import tokenize
from nltk.tokenize import word_tokenize
from summarizer.algorithms.scoring import scoring_algorithm

def getWords(sentence):
    """
    Extracts words/tokens from a sentence
    :param sentence: (str) sentence
    :returns: list of tokens
    """
    words = word_tokenize(sentence)
    return words

def getParagraphs(content):
    """
    Exctracts paragraphs from the the text content
    :param content: (str) text content
    :returns: list of paragraphs
    """
    paraList = content.split('\n\n')
    return paraList

def getSentences(paragraph):
    """
    Extracts sentences from a paragraph
    :param paragraph: (str) paragraph text
    :returns: list of sentences
    """
    sentence_list = tokenize.sent_tokenize(paragraph)
    return sentence_list

def getNepSentences(paragraph):
    # return re.split(u'।', paragraph)
    return re.split('(?<=[।?!]) +', paragraph)

def sort_and_print(body, num):
    """
    Sorts the values of dictionaries and prints respective
    top sentences
    :param body: list of dictionaries of 'sentence': score
    :param num: no of sentences to be printed
    :return: prints
    """
    result = []
    rank = []
    for sentdict in body:
        for sent in sentdict:
            rank.append(sentdict[sent])

    rank = list(set(rank))  # remove duplicates
    rank = sorted(rank, reverse=True)

    count = 0
    # print top 'num' sentences in same order as of original document

    for sentdict in body:
        for sent in sentdict:
            if count == num:
                break
            for r in rank[:num]:
                if sentdict[sent] == r:
                    result.append(sent)
                    count += 1
    return result

def clean_text(text):
    """
    Cleans the text by removing repeated phrases and irrelevant information.
    :param text: (str) text to clean
    :returns: (str) cleaned text
    """
    # Remove repeated phrases
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    
    # Remove navigation links and other irrelevant information
    text = re.sub(r'British Broadcasting Corporation.*?Contact technical support', '', text, flags=re.DOTALL)
    
    return text

def summarize_text(text, sentence_no=5):
    """
    Summarizes the text using the scoring algorithm.
    :param text: (str) text to summarize
    :param sentence_no: (int) number of sentences in the summary
    :returns: (str) summarized text
    """
    result_list = scoring_algorithm.scoring_main(text, sentence_no)
    summary = ' '.join(result_list)
    return summary
