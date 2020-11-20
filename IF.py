#影响因子的计算
import re
import requests
from bs4 import BeautifulSoup
import time
times = 0
times2 = 0
times3 = 0
# 使用异常处理，捕获相关异常，e.g. 访问异常
def my_soup(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 ' \
                          '(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 ' \
                          '(KHTML, like Gecko) Version/5.1 Safari/534.50'
    Url = url
    res = requests.get(Url, headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    return soup

for i in range(1, 6):
    url = 'http://apps.webofknowledge.com/summary.do?product=UA&parentProduct=UA&search_mode=GeneralSearch&parentQid=1&qid=2&SID=8A9Op8FZawko7D1IwSm&&update_back2search_link_param=yes&page={}'.format(i)
    soup = my_soup(url)
    for item in soup.find_all('a', {'class': 'snowplow-times-cited-link'}):
        paper_url = 'http://apps.webofknowledge.com' + item.get("href")
        the_soup = my_soup(paper_url)
        
        
        for item2 in the_soup.find_all('a', {'name': 'CAScorecard_link_WOS_classic'}):
            paper_url2 = 'http://apps.webofknowledge.com/' + item2.get("href")   
            ssoup = my_soup(paper_url2)
            for item in ssoup.find_all('div', {'class': 'refine-subitem-title'}):
                if '2020 (' in item.getText():
                    temp2 = item.getText()[8:-2] # 上线后，不能用死的索引，推荐用正则表达式优化
                    times2 = times2 + int(temp2)
        print('1/3 finished')
        for item3 in the_soup.find_all('a', {'name': 'CAScorecard_link_WOS_ESCI'}):
            paper_url3 = 'http://apps.webofknowledge.com/' + item3.get("href")
            ssoup = my_soup(paper_url3)
            for item in ssoup.find_all('div', {'class': 'refine-subitem-title'}):
                if '2020 (' in item.getText():
                    temp3 = item.getText()[8:-2]
                    times3 = times3 + int(temp3)
        print('2/3 finished')
        for item1 in the_soup.find_all('a', {'name': 'CAScorecard_link_WOS'}):
            paper_url1 = 'http://apps.webofknowledge.com/' + item1.get("href")        
            ssoup = my_soup(paper_url1)
            for item in ssoup.find_all('div', {'class': 'refine-subitem-title'}):
                if '2020 (' in item.getText():
                    temp = item.getText()[8:-2]                    
                    times = times + int(temp)
    
print("wos核心集次数="+str(times))        

print("SCIE，SSCI的次数="+str(times2))        

print("ESCI的次数="+str(times3))        

print("SCIE，SSCI+ESCI的次数之和="+str(times2+times3))        

print("影响因子的计算wos"+str(times/50.0))  

print("影响因子的计算（SCIE，SSCI+ESCI的次数之和）"+str((times2+times3)/50.0))  
