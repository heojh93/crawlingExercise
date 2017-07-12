#-*- coding: utf-8 -*-

import urllib
import urllib.request
import re
import csv

# Print result as a xlsx format
import xlsxwriter

from bs4 import BeautifulSoup
from selenium import webdriver


# Get logaDB's Search Page
def getPage(targetUrl):

    url = 'http://www.logadb.com/search/search.php?s_sec=fir&pg_mode=search&bad1=1&bad3=1&t_search_value=' + targetUrl
    print(url)
    source_code = urllib.request.urlopen(url)
    plain_text = source_code.read()
    soup = BeautifulSoup(plain_text, 'html.parser')
    return soup


# Crawling
def logaCrawl(xlsx):

    # It needs to use webdriver because of
    # 1. accessing iframe page and
    # 2. logaDB's security process.
    browser = webdriver.Chrome('C:/Users/Heoju/Desktop/crawler/chromedriver')

    # variables for xlsx
    xrow = 1
    xcol = 0

    with open("./temp.csv", "r", encoding='utf-8') as csvFile:
        
        data = csv.DictReader(csvFile)

        for row in data:
            url = row['url']
            name = row['name']
            print(url)
            print(name)
            browser.get('http://www.logadb.com/search/search.php?s_sec=fir&pg_mode=search&bad1=1&bad3=1&t_search_value=' + url)
            browser.switch_to_frame(browser.find_element_by_tag_name("iframe"));
            plain_text = browser.page_source

            _soup = BeautifulSoup(plain_text, 'html.parser')

            # Divide case as searching result exists or not.
            if _soup.find("td",{"class" : "com_r01"}) :
                table = _soup.find("td",{"class" : "com_r01"}).parent.parent
                
                adPrice = table.find_all("tr")[4]
                naver_premium = adPrice.find_all("td")[1].get_text()
                naver_normal = adPrice.find_all("td")[2].get_text()
                daum_premium = adPrice.find_all("td")[3].get_text()
                daum_normal = adPrice.find_all("td")[4].get_text()

                # Insert data at xlsx file
                xlsx.write(xrow, xcol, name)
                xlsx.write(xrow, xcol+1, url)
                xlsx.write(xrow, xcol+2, naver_premium)
                xlsx.write(xrow, xcol+3, naver_normal)
                xlsx.write(xrow, xcol+4, daum_premium)
                xlsx.write(xrow, xcol+5, daum_normal)
                
                #writer.writerow([name, url])
                #writer.writerow([naver_premium, naver_normal, daum_premium, daum_normal])
                #print(naver_premium + ', ' + naver_normal + ', ' + daum_premium + ', ' + daum_normal)
                
            else:
                print("no information")

            xrow += 1
            
    browser.quit()
