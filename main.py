import re
import requests
from bs4 import BeautifulSoup
import datetime
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
import time
# import pandas_datareader.data as web

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import chromedriver_binary
# import time

# url = 'https://www.kabuyutai.com/yutai/september.html'

# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

# driver.get(url)
# time.sleep(10)
# print(driver.current_url)
# print(driver.page_source)
# soup = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()

columns = ['date', 'url']
df_url = pd.DataFrame(columns=columns)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

url = "https://www.nikkei.com/markets/kabu/index/?uah=DF_SEC8_C1_050"

i = 1
max = 50
while True:
    if i > 1:
        url = "https://www.nikkei.com/markets/kabu/index/?bn=" + str((i-1)*30 + 1) + "&uah=DF_SEC8_C1_050"

    print(url)
    r= requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup.prettify())
    table_elms = soup.select('li.m-article_list_title')

    for table_elm in table_elms:
        span = table_elm.select_one('span.m-article_title-time') 
        # print(span.get_text())
        # print(table_elm.a['href'])
        redate = re.findall('(?<=（).*?(?=）)', span.get_text())
        url = 'https://www.nikkei.com' + table_elm.a['href']
        print(redate[0])
        date = redate[0]
        print(len(date))

        if len(date) < 6:
            date = '2023/' + date
        
        print(date)
        print(url)
        df_tmp = pd.DataFrame(data = [[date, url]], columns = columns)
        df_url = pd.concat([df_url, df_tmp], ignore_index=True)

    i = i + 1
    time.sleep(0.5)

    if i > max:
        break

print(df_url)
df_url.to_csv('50.csv')