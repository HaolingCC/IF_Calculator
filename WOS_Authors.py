import re
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from retrying import retry


def _result(result):
    return result is None

@retry(stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000, retry_on_result=_result)
def new_request_get(url, headers=None):
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code != 200:
            raise requests.RequestException('my_request_get error!!!!')
        return response


def my_soup(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 ' \
                          '(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 ' \
                          '(KHTML, like Gecko) Version/5.1 Safari/534.50'
    Url = url
    res = new_request_get(Url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    return soup



def select2020(url):
    driver = webdriver.Chrome()
    driver.get(url)
    a = driver.find_element_by_id('PublicationYear_1')
    if '2020'in a.get_attribute('value'):
        a.click()
        driver.find_element_by_css_selector(".refine-button").click()
        newurl = driver.current_url
        return newurl



def get_cell_paper_info(url):    
    cell_paper_url=url
    cell_soup = my_soup(cell_paper_url)
    authors=[]
    for k in cell_soup.find_all('a', {'title': 'Find more records by this author'}):
        author = k.getText().strip()
        authors.append(author)
    return authors


def get_url_list1(url):
    paper_url = url
    paper_soup = my_soup(paper_url)
    wos_num = paper_soup.find('span', {'id': 'CAScorecard_count_WOS'}).getText()
    n = int(wos_num)   
        
    if n ==0:
        return []    
    

    halfurl = (paper_soup.find('a', {'class': 'smallV110 snowplow-full-record'}).get("href"))
    item_url = 'http://apps.webofknowledge.com/' + halfurl
    url_list = []
    
    print(n)
    for i in range(1,n+1):
        url_list.append(item_url.replace('doc=1','doc='+str(i))) 
        
    return url_list



authorsTotal=[]
for i in range(1, 6):
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=1&qid=2&SID=5CLAluCVLb3ivwHKQGo&&update_back2search_link_param=yes&page={}'.format(i)
    soup = my_soup(url)
    for item in soup.find_all('a', {'class': 'snowplow-times-cited-link'}):
        paper_url = 'http://apps.webofknowledge.com' + item.get("href")
        paper_soup = my_soup(paper_url)
       
    
    #if！=0
        
        for item1 in paper_soup.find_all('a', {'name': 'CAScorecard_link_WOS'}):
            paper_url1 = 'http://apps.webofknowledge.com/' + item1.get("href")
        
            new = select2020(paper_url1)
            
            if new is None: 
                break
            
            m = get_url_list1(new)
        
            for paper in m:
                print(get_cell_paper_info(paper))
                for author in get_cell_paper_info(paper):
                    authorsTotal.append(author)

print(authorsTotal)

import xlwt
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('1')

# 参数对应 行, 列, 值

for i in range (len(authorsTotal)):
    worksheet.write(i,0, label = authorsTotal[i])


workbook.save('authors.xls')

