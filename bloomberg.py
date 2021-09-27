from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import re

# 크롬 창을 띄우지 않고 실행하는 옵션
chrome_option = webdriver.ChromeOptions()
chrome_option.add_argument('headless')
chrome_option.add_argument("disable-gpu")

# 셀레니움 웹드라이버 실행
driver = webdriver.Chrome('chromedriver', options=chrome_option)
driver.implicitly_wait(5)
time.sleep(20)

# 블룸버그 백신정보 url
url_corona = 'https://www.bloomberg.com/graphics/covid-vaccine-tracker-global-distribution/'

# 웹드라이버 실행
driver.get(url_corona)
driver.implicitly_wait(5)
time.sleep(10)

# 더보기 버튼

show_more = driver.find_element_by_xpath('//*[@id="dvz-table-global-vaccination"]/div[2]/div[2]/button')
show_more.click()
driver.implicitly_wait(5)
show_more.click()
driver.implicitly_wait(5)

time.sleep(10)

# 페이지 소스 받아와서 bs로 parse
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')
driver.implicitly_wait(5)

# 정보 담을 list 생성
information = [[] for i in range(6)]

# 백신 정보 테이블 찾기
country_table = soup.find('table', class_='svelte-1jr5wu3').find('tbody')

# 나라 리스트
country_list = country_table.find_all('tr')

for country in country_list:
    info_list = country.find_all('td')
    index = 0
    for info in info_list:
        text = info.text
        text = text.replace(',', '').replace('<', '')
        information[index].append(text)
        index += 1

# 오늘 날짜
now = datetime.datetime.now()
now_date = now.strftime('%Y-%m-%d')

# 파일명 정하기
file_name = f'./data/bloomberg({now_date}).csv'

dict_info = {'Countries and regions':information[0],
             'Doses administered':information[1],
             'Enough for % of people':information[2],
             'given 1+ dose':information[3],
             'fully vaccinated':information[4],
             'Daily rate of doses administered':information[5]}

corona_info = pd.DataFrame(dict_info)
corona_info.to_csv(file_name, index=False, encoding='utf-8-sig')


# 드라이버 창 닫기
driver.quit()