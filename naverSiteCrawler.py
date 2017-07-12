#-*- coding: utf-8 -*-

import urllib
import urllib.request
import re
import csv

from bs4 import BeautifulSoup


exclude = ['instagram', 'facebook', 'google', 'naver', 'youtube', 'daum', 'twitter',
           'blog', 'tistory', '.or.','.ac', '.org/', 'edu','gov', 'asiae.co.kr',
           '.sbs.', '.kbs.', '.ebs.', '.imbc.','apple', 'mnet', 'egloos']

query = input()

# Remove Tag
def cleanTag(raw_html):

    clean = re.compile('<.*?>')
    txt = re.sub(clean, '', raw_html)
    return txt


# Parse Pages with BeautifulSoup
def parsing(page):

    searchUrl = 'https://search.naver.com/search.naver?where=site&sm=tab_jum&ie=utf8&query='
    pageUrl = '&start='+ str(10*(page-1)+1)

    # Encoding issue when URL has Korean word : urllib.parse.quote
    url = searchUrl + str(urllib.parse.quote(query)) + pageUrl
    source_code = urllib.request.urlopen(url)
    plain_text = source_code.read()
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup


# Find the number of pages which need to be crawled
def maxPage():

    soup = parsing(1)

    if soup.find("div", {"not_found02"}):
        print("결과가 없습니다\n");
        return 0

    else:
        number = soup.find("span", {"class" : "title_num"}).string
        x = re.search(r'.*\/ (.*?)건', number).group(1)
        number = ''.join(c for c in x if c.isdigit())
        return (int(number)-1)/10 +1


# Crawling
def crawl(max_pages):

    page = 1

    with open("./temp.csv","w",encoding="utf-8") as csvFile:
        fieldnames = ['name', 'url']
        data = csv.DictWriter(csvFile, fieldnames = fieldnames)
        data.writeheader()

        while page <= max_pages:
            soup = parsing(page)
            element = soup.find("ul",{"class":"type01"})

            for list in element.findAll('li'):
                name = list.a

                # Filter
                if not any(e in str(name["href"]) for e in exclude):
                    data.writerow({'name' : str(cleanTag(str(name))), 'url' : str(name['href'])})
                    
            page +=1
    return query
