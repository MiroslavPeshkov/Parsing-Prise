import requests
from bs4 import BeautifulSoup
import time
import streamlit as st
import csv
import pandas as pd
import re
import lxml
import re
from lxml import html
import datetime
import selenium

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
# chromeOptions = webdriver.ChromeOptions()
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as FirefoxOptions

firefoxOptions = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
# firefoxOptions.add_argument(f'user-agent={user_agent}')
firefoxOptions.binary_location = "/usr/bin/firefox"
firefoxOptions.add_argument('--headless')
firefoxOptions.add_argument('--no-sandbox')
#firefoxOptions.add_argument('--log-level=3')
firefoxOptions.add_argument("--window-size=1920,1080")
firefoxOptions.add_argument('--disable-dev-shm-usage')
#firefoxOptions.add_argument("--start-maximized")
firefoxOptions.add_argument('--ignore-certificate-errors')
firefoxOptions.add_argument('--allow-running-insecure-content')
import os, sys
import numpy as np

path = os.getcwd()
# print(path)
st.write(path)

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver.exe')

_ = installff()

st.title('Парсинг цен')
st.subheader("Контейнер для загрузки Excel")
uploadedFile = st.file_uploader("Загрузите txt file",  type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
if uploadedFile is not None:
    df = pd.read_excel(uploadedFile)
    name = df['Артикул, марка '].tolist()
    articl = df['Наименование'].tolist()
    all_name = [[i, j] for i, j in zip(articl, name)]
    s_all = []
    for i in range(len(all_name)):
        if type(all_name[i][1]) == str:
            s_all.append(all_name[i][1])
        elif all_name[i][1] is np.nan:
            all_name[i][1] = all_name[i][0]
            s_all.append(str(all_name[i][1]))
    s_all_final = []
    for i in s_all:
        if i == 'nan':
            continue
        else:
            s_all_final.append(i)
    s_all_final = list(map(lambda x: x.replace('\n', ''), s_all_final))
    s_all_final = s_all_final[10:14]

    st.write('Begin')
    good_links = {}
    for goods in s_all_final:
        good_links[goods] = []


        # THE FIRST SITE
        url_1 = f'https://www.tinko.ru/search?q={goods}'
        res = requests.get(url_1)
        soup = BeautifulSoup(res.text, 'lxml')
        links = soup.find_all('p', {'class', 'catalog-product__title'})
        links_ = [i.find('a') for i in links]
        links_all = ['https://www.tinko.ru' + i.get('href') for i in links_]
        for l in links_all:
            st.write('Now - ', l, 'for goods - ', goods)
            r = requests.get(l)
            soup = BeautifulSoup(r.text, 'lxml')
            try:
                first_pattern = soup.find('h1').text
                second_pattern = soup.find('h2').text
            except Exception as ex:
                st.write(ex)
                st.write(l)
            if goods in first_pattern or goods in second_pattern:
                st.write('Yes price')
                try:
                    price = soup.find('span', {'class', 'product-detail__price-value'}).text.replace(' ', '').replace(
                        ',', '.')
                    st.write(price, 'for site - ', l)
                    good_links[goods].append(price)
                    break
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                    break
            else:
                continue


        # THE SECOND SITE
        url_2 = f"https://videoglaz.ru/?digiSearch=true&term={goods}&params=%7Csort%3DDEFAULT"
        browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options = firefoxOptions)
        browser.implicitly_wait(7)
        browser.get(url_2)
        time.sleep(10)
        html = browser.page_source
        soup_ = BeautifulSoup(html, 'lxml')
        links = soup_.find_all('div', {'class': 'digi-product'})
        links_ = [i.find('a') for i in links]
        links_all = ['https://videoglaz.ru' + i.get('href') for i in links_]
        for l in links_all:
            st.write('Now - ', l, 'for goods - ', goods)
            res = requests.get(l)
            soup = BeautifulSoup(res.text, 'lxml')
            try:
                first_pattern = soup.find('h1', {'class': 'm-0 good-title'}).text
                second_pattern = soup.find('div', {'class': 'tab-content m-3'}).text
            except Exception as ex:
                st.write(ex)
                st.write(l)
            if goods in first_pattern or goods in second_pattern:
                st.write('Yes price')
                try:
                    price = soup.find('div', {'class': 'cenaWrap'}).find('b').text.replace(' ', '').replace(',', '.')
                    st.write(price, 'for site - ', l)
                    good_links[goods].append(price)
                    break
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                    break
            else:
                continue


        # THE THIRD SITE
        url_3 = f'https://www.citilink.ru/search/?text={goods}'
        browser = webdriver.Chrome(executable_path=r'/home/appuser/geckodriver.exe', options = firefoxOptions)
        browser.implicitly_wait(2)
        browser.get(url_3)
        time.sleep(3)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('a', {'class': 'ProductCardVertical__name Link js--Link Link_type_default'})
        links_all = ['https://www.citilink.ru' + i.get('href') for i in links]
        for l in links_all[:10]:
            st.write('Now - ', l, 'for goods - ', goods)
            browser.get(l)
            time.sleep(4)
            html = browser.page_source
            time.sleep(2)
            soup = BeautifulSoup(html, 'lxml')
            try:
                first_pattern = soup.find('h1').text
            except Exception as ex:
                st.write(ex)
                st.write(l)
            if goods in first_pattern:
                st.write('Yes price')
                try:
                    price = soup.find('span', {
                        'class': "ProductPrice__price ProductCartFixedBlockNEW__price__price"}).text.replace('\n',
                                                                                                             '').replace(
                        '₽', '').replace(' ', '').replace(',', '.').strip()
                    st.write(price, 'for site - ', l)
                    good_links[goods].append(price)
                    break
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                    break
            else:
                continue


        # THE FORTH SITE
        url_4 = f'https://www.xcom-shop.ru/?digiSearch=true&term={goods}&params=%7Csort%3DDEFAULT'
        browser = webdriver.Chrome(executable_path=r'/home/appuser/geckodriver.exe', options = firefoxOptions)
        browser.implicitly_wait(2)
        browser.get(url_4)
        time.sleep(3)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('div', {'class': 'digi-product'})
        links_ = [i.find('a') for i in links]
        links_all = ['https://www.xcom-shop.ru' + i.get('href') for i in links_]
        for l in links_all:
            st.write('Now - ', l, 'for goods - ', goods)
            browser = webdriver.Chrome(executable_path=r'/home/appuser/geckodriver.exe', options = firefoxOptions)
            browser.implicitly_wait(2)
            browser.get(l)
            time.sleep(2)
            html = browser.page_source
            time.sleep(2)
            soup = BeautifulSoup(html, 'lxml')
            try:
                first_pattern = soup.find('h1').text
            except Exception as ex:
                st.write(ex)
                st.write(l)
            if goods in first_pattern:
                st.write('Yes price')
                try:
                    price = soup.find('div', {'class': "card-bundle-basket__price"}).text.split('\n')[0].replace('₽',
                                                                                                                 '').replace(
                        ' ', '').replace(',', '.').strip()
                    st.write(price, 'for site - ', l)
                    good_links[goods].append(price)
                    break
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                    break
            else:
                continue

        # THE FIFTH SITE
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.'}
        url_5 = f'https://www.etm.ru/catalog?searchValue={goods}&rows=12'
        r = requests.get(url_5, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        links = soup.find_all('a', {'target': '_self'})
        links_all = ['https://www.etm.ru' + i.get('href') for i in links]
        for l in links_all:
            st.write('Now - ', l, 'for goods - ', goods)
            res = requests.get(l, headers=headers)
            soup = BeautifulSoup(res.text, 'lxml')
            try:
                first_pattern = soup.find('h1').text
                second_patter = soup.find('p', {'class', 'jss86'}).text
            except Exception as ex:
                st.write(ex)
                st.write(l)
            if goods in first_pattern or goods in second_patter:
                st.write('Yes price')
                try:
                    price = soup.find(text=re.compile('Ваша цена')).find_next('p').text.replace('₽', '').replace(',',
                                                                                                                 '.').replace(
                        ' ', '')
                    st.write(price, 'for site - ', l)
                    good_links[goods].append(price)
                    break
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                    break
            else:
                continue

    dict_2 = {}
    for k, v in good_links.items():
        flot_no = list(filter(None, v))
        if len(flot_no) > 0:
            len_ = len(flot_no)
            list_ = list(map(float, flot_no))
            sum_ = sum(list_)
            avarage = sum_ / len_
            dict_2[k] = avarage

    df = pd.DataFrame.from_dict(dict_2, orient='index', columns=['Средняя цена товара'])
    df.index.name = 'Название товара'
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    writer = pd.ExcelWriter(f'Парсинг цен - {now_date}.xlsx')
    df.to_excel(writer, index=True)
    writer.save()

    st.write('CSV done')

    with open(f'Парсинг цен - {now_date}.xlsx', "rb") as file:
        st.download_button(
            label="Download data as CSV",
            data=file,
            file_name=f'Парсинг цен - {now_date}.xlsx',
            mime='text/xlsx',
        )







