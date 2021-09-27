from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time
from datetime import date, timedelta
import pandas as pd
import re

# 크롬 창을 띄우지 않고 실행하는 옵션
chrome_option = webdriver.ChromeOptions()
#chrome_option.add_argument('headless')
chrome_option.add_argument("disable-gpu")

# 셀레니움 웹드라이버 실행
driver = webdriver.Chrome('chromedriver', options=chrome_option)
driver.implicitly_wait(5)

# 코로나보드 url
url_corona = 'https://coronaboard.kr/'

# 웹드라이버 실행
driver.get(url_corona)
driver.implicitly_wait(5)
time.sleep(3)

#어제 버튼 클릭
btn_yesterday = driver.find_element_by_xpath('//*[@id="global-slide"]/div/div[2]/ul/li[2]/a')
btn_yesterday.click()

# 모든 속성 누르기
btn_dropdown = Select(driver.find_element_by_xpath('//*[@id="picker-global-table"]'))
btn_dropdown.select_by_index(0)
btn_dropdown.select_by_index(1)
btn_dropdown.select_by_index(5)

# 더보기 버튼
show_more = driver.find_element_by_xpath('//*[@id="show-more"]')
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

information = [[] for i in range(11)]

# 코로나 정보 테이블 찾기
country_table = soup.find('div', id='country-table').find('tbody')

# 나라 리스트
country_list = country_table.find_all('tr')

for country in country_list:
    info_list = country.find_all('td')
    index = 0
    for info in info_list:
        text = info.text
        text = text.replace(',', '')
        text = re.sub('[(].*[)]', '', text)
        information[index].append(text)
        index += 1

# 어제 날짜
yesterday = date.today() - timedelta(1)
yesterday = yesterday.strftime('%Y-%m-%d')

# 파일명 정하기
file_name = f'./data/coronaboard({yesterday}).csv'

dict_info = {'국가':information[1],
             '확진자':information[2],
             '치료중':information[3],
             '위중증':information[4],
             '사망자':information[5],
             '완치':information[6],
             '치명(%)':information[7],
             '완치(%)':information[8],
             '발생률':information[9],
             '인구수':information[10]}

corona_info = pd.DataFrame(dict_info)
corona_info.to_csv(file_name, index=False, encoding='utf-8-sig')

# 드라이버 창 닫기
driver.quit()