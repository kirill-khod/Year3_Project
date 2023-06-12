from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
import time
import undetected_chromedriver as uc
from selenium_stealth import stealth
import csv
import re
import spacy

#import undetected_chromedriver as uc
# import seleniumwire.undetected_chromedriver as uc
import undetected_chromedriver as uc

import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def to_txt(my_list, col):
    if col==0:
        for i in range(0, len(my_list)):
            my_list[i] = my_list[i].text
    elif col==1:
        for i in range(0, len(my_list)):
            my_list[i] = my_list[i].text.replace('\n', " ")
    elif col==2:
        for i in range(0, len(my_list)):
            my_list[i] = re.sub("[^0-9]", "", my_list[i].text)
    return my_list


def navigate(driver, url, page_no):
    driver.get(url)


def get_data(driver, class_name):
    return driver.find_elements(By.XPATH, class_name)


def has_data(data):
    return len(data) > 0

options = uc.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")
# # options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(options=options)
#
# stealth(driver,
#         user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         )



# options = Options()
# options.add_argument('-disable-infobars')
#options.add_argument('--headless=new')
# driver = webdriver.Chrome(options=options)
url = "https://www.ozon.ru/category/smartfony-15502/"
# # url = "https://www.ozon.ru/category/noutbuki-15692/"
flag = True
label = []
descr = []
price = []
category = []
link = []
categ=""

for i in range(0, 31):
    if flag:
        driver.get(url)
        categ = str(to_txt(get_data(driver, "//a[@class='yd8 j7e']/span"), 0)[0]) + ',' + str(to_txt(get_data(driver, "//h1[@class='g2e']"), 0)[0])
        flag=False
    else:
        driver.get(driver.find_element(By.XPATH, "//a[@class='a2-a4']").get_attribute('href'))

    time.sleep(12)
    label += to_txt(get_data(driver, "//span[@class='v0d d1v v1d v3d tsBodyL ki9 li']/span"), 0)
    descr += to_txt(get_data(driver, "//span[@class='u8d d9u d2v tsBodyM ik7']/span"), 1)
    # price += to_txt(get_data(driver, "//div[@class='c7']//div[@class='d6-a ki9']/div[@class='d6-a0'] | //div[@class='c7']//div[@class='d6-a ki9']/span[@class='d7-a2']"), 2)
    price += to_txt(get_data(driver, "//div[@class='c7']//div[@class='d6-a ki9']/div[@class='d6-a0'] | //div[@class='c7']//span[@class='d7-a3 d7-a7 d7-b']/span[@class='d7-a2']"), 2)
    for j in range(len(label)):
        category.append(categ)
    data4_href = driver.find_elements(By.XPATH, "//a[@class='tile-hover-target ki9 li']")
    for href in data4_href:
        link.append(href.get_attribute("href"))
    print(i)

#//div[@class='oi0'] | //div[@class='oi0 o0i']  | //div[@class='o2i']



# rows = zip(label, descr, price, link)
rows = zip(label, price, category, link)
with open('makiyazh2.csv', "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)



# print("page2")
#
# time.sleep(12)
#
# # url = "https://www.ozon.ru" + get_data(driver, "//a[@class='a2-a4']/href").text
# driver.get(driver.find_element(By.XPATH, "//a[@class='a2-a4']").get_attribute('href'))
# time.sleep(12)
# data3 = get_data(driver, "//span[@class='u8d d9u u9d d1v tsBodyL ik7 k7i']/span")
#
# for i in range(0, len(data3)):
#     print(data3[i].text)
#
# print("page3")
#
# time.sleep(12)
# driver.get(driver.find_element(By.XPATH, "//a[@class='a2-a4']").get_attribute('href'))
# time.sleep(12)
# data4 = get_data(driver, "//span[@class='u8d d9u u9d d1v tsBodyL ik7 k7i']/span")
# for i in range(0, len(data4)):
#     print(data4[i].text)



driver.close()
