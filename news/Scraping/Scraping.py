# news/Scraping/Scraping.py

from pprint import pprint
import re
from bs4 import BeautifulSoup
import requests
from summarizer.algorithms.scoring import scoring_algorithm, scoring_nepali
from summarizer.algorithms.scoring.util import clean_text, summarize_text

def bbc_scraping():
    page = requests.get("https://www.bbc.com/news")
    soup = BeautifulSoup(page.content, 'html.parser')
    newsDict = dict()

    div = soup.find('div', class_="nw-c-most-read__items gel-layout gel-layout--no-flex")
    if div is None:
        print("Could not find the most-read items div.")
        return newsDict

    newslist = div.find_all('div', class_="gs-o-media__body")
    if not newslist:
        print("Could not find any news items.")
        return newsDict

    for i in range(5):
        news = newslist[i].a['href']
        news1 = 'https://www.bbc.com' + news
        page1 = requests.get(news1)
        soup1 = BeautifulSoup(page1.content, 'html.parser')

        heading = soup1.find('h1', class_='story-body__h1')
        if heading is None:
            print("Could not find the heading.")
            continue

        body_div = soup1.find('div', class_='story-body__inner')
        if body_div is None:
            print("Could not find the body div.")
            continue

        body_paragraphs = body_div.find_all('p')
        body = ''
        for p in body_paragraphs:
            body += '\n' + p.get_text()

        # Clean the text
        body = clean_text(body)
        
        # Summarize the text
        summary = summarize_text(body)

        newsDict[heading.get_text()] = summary

    return newsDict

def cnn_scraping():
    page = requests.get("http://rss.cnn.com/rss/edition.rss")
    soup = BeautifulSoup(page.content, features="xml")
    items = soup.find_all('item')
    newsDict = dict()
    titles = []
    links = []
    for i in items[:5]:
        titles.append(i.title.get_text())
        links.append(i.link.get_text())

    for count, l in enumerate(links):
        page1 = requests.get(l)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        pg = ''
        if re.match(r'^https://money.cnn', l) is not None:
            body_div_m = soup1.find('div', class_='storytext')
            body_p = body_div_m.find_all('p')
            for p in body_p:
                pg = pg + '\n' + p.get_text()
        else:
            body_div = soup1.find_all('div', class_='zn-body__paragraph')
            for div in body_div:
                pg = pg + '\n' + div.get_text()
        
        # Clean the text
        pg = clean_text(pg)
        
        # Summarize the text
        summary = summarize_text(pg)
        
        newsDict[titles[count]] = summary
    return newsDict

def nagarik_scraping():
    page = requests.get("https://nagariknews.nagariknetwork.com/")
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the div with class "col-sm-4 title-second"
    div = soup.find('div', class_="col-sm-4 title-second")

    # Check if the div is None
    if div is None:
        raise ValueError("The 'col-sm-4 title-second' div was not found. The structure of the page might have changed.")

    # Proceed if div is found
    links = div.find_all('a', class_=lambda x: x != "heading-link")
    newsDict = dict()
    titles = []
    body_links = []
    
    # Check if there are enough links (at least 5)
    if len(links) < 5:
        raise ValueError("Not enough links found. Check the page structure.")

    for i in range(5):
        titles.append(links[i].get_text())
        body_links.append('https://nagariknews.nagariknetwork.com' + links[i].get('href'))

    for count, l in enumerate(body_links):
        page1 = requests.get(l)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        
        # Find the div with id="newsContent"
        div1 = soup1.find(id="newsContent")

        # Check if div1 is None
        if div1 is None:
            raise ValueError(f"Could not find content in {l}. Check if the page structure has changed.")

        pgs = div1.find_all('p')
        body = ''
        for p in pgs:
            body = body + '\n\n' + p.get_text()
        
        # Clean the text
        body = clean_text(body)
        
        # Use the scoring function to summarize
        summary = summarize_text(body, sentence_no=5)
        
        newsDict[titles[count]] = summary

    return newsDict
