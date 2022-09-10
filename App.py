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
from shutil import which
import os, sys
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

firefoxOptions = Options()
FIREFOXPATH = which("firefox")
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
firefoxOptions.add_argument(f'user-agent={user_agent}')
firefoxOptions.add_argument('--headless')
firefoxOptions.add_argument('--no-sandbox')
firefoxOptions.add_argument("--window-size=1920,1080")
firefoxOptions.add_argument('--disable-dev-shm-usage')
firefoxOptions.add_argument('--ignore-certificate-errors')
firefoxOptions.add_argument('--allow-running-insecure-content')
firefoxOptions.add_argument('--disable-blink-features=AutomationControlled')
firefoxOptions.binary = FIREFOXPATH
path = os.getcwd()

@st.experimental_singleton
def installff():
    os.system('sbase install geckodriver')
    os.system(
        'ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver.exe')
_ = installff()

def scrapping_avarage_price(s_all_final):
    st.write('Begin scrapping')
    good_links = {}
#     browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options=firefoxOptions)
    for goods in s_all_final:
        good_links[goods] = []
        try:
            # THE FIRST SITE
            url_1 = f'https://www.tinko.ru/search?q={goods}'
            res = requests.get(url_1)
            time.sleep(1.5)
            soup = BeautifulSoup(res.text, 'lxml')
            links = soup.find_all('p', {'class', 'catalog-product__title'})
            links_ = [i.find('a') for i in links]
            links_all = ['https://www.tinko.ru' + i.get('href') for i in links_]
            st.write(len(links_all))
            len_ = int(round((len(links_all) - 5) / 2, 0))
            st.write(len_)
            for l in links_all[:int(round((len(links_all) - 5) / 2, 0))]:
                st.write('Now - ', l, 'for goods - ', goods)
                r = requests.get(l)
                time.sleep(1.5)
                soup = BeautifulSoup(r.text, 'lxml')
                try:
                    first_pattern = soup.find('h1').text.replace('\n', '').replace('\t', '')
                    st.write(first_pattern.lower().strip() , '==', goods.lower().strip())
                    second_pattern = soup.find('h2').text.replace('\n', '').replace('\t', '')
                    st.write(second_pattern.lower().strip(), '==', goods.lower().strip())
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                if goods.lower().strip() in first_pattern.lower().strip() or goods.lower().strip() in second_pattern.lower().strip():
                    st.write('Yes price')
                    try:
                        price = soup.find('span', {'class', 'product-detail__price-value'}).text.replace(' ',
                                                                                                         '').replace(
                            ',', '.')
                        st.write(price, 'for site - ', goods)
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
            browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options=firefoxOptions)
            browser.implicitly_wait(7)
            browser.get(url_2)
            time.sleep(5)
            html = browser.page_source
            soup_ = BeautifulSoup(html, 'lxml')
            links = soup_.find_all('div', {'class': 'digi-product'})
            links_ = [i.find('a') for i in links]
            links_all = ['https://videoglaz.ru' + i.get('href') for i in links_]
            st.write(len(links_all))
            browser.quit()
            len_ = int(round((len(links_all) - 5) / 2, 0))
            st.write(len_)
            for l in links_all[:int(round((len(links_all) - 5) / 2, 0))]:
                st.write('Now - ', l, 'for goods - ', goods)
                res = requests.get(l)
                time.sleep(1.5)
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
                        price = soup.find('div', {'class': 'cenaWrap'}).find('b').text.replace(' ', '').replace(',',
                                                                                                                '.')
                        st.write(price, 'for site - ', goods)
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
            browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options = firefoxOptions)
            browser.implicitly_wait(2)
            browser.get(url_3)
            time.sleep(3)
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            links = soup.find_all('a', {'class': 'ProductCardVertical__name Link js--Link Link_type_default'})
            links_all = ['https://www.citilink.ru' + i.get('href') for i in links]
            for l in links_all[:5]:
                st.write('Now - ', l, 'for goods - ', goods)
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
                    try:
                        price = soup.find('span', {
                            'class': "ProductPrice__price ProductCartFixedBlockNEW__price__price"}).text.replace('\n',
                                                                                                                 '').replace(
                            '₽', '').replace(' ', '').replace(',', '.').strip()
                        st.write(price, 'for site - ', goods)
                        good_links[goods].append(price)
                        break
                    except Exception as ex:
                        st.write(ex)
                        st.write(l)
                        break
                else:
                    continue
            browser.quit()

            # THE FORTH SITE
            url_4 = f'https://sort.diginetica.net/search?st={goods}&apiKey=D1K76714Q4&strategy=vectors_extended,zero_queries_predictor&fullData=true&withCorrection=true&withFacets=true&treeFacets=true&regionId=global&useCategoryPrediction=true&size=20&offset=0&showUnavailable=true&unavailableMultiplier=0.2&preview=false&withSku=false&sort=DEFAULT'
            res = requests.get(url_4)
            time.sleep(2)
            res = res.text
            js = json.loads(res)
            js = js['products']
            for good in js:
                name = good['name']
                if goods in name:
                    price = good['price']
                    st.write(price, 'for site - ', goods)
                    good_links[goods].append(price)
                    break

            # THE FIFTH SITE
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.'}
            url_5 = f'https://www.etm.ru/catalog?searchValue={goods}&rows=12'
            r = requests.get(url_5, headers=headers)
            time.sleep(1.5)
            soup = BeautifulSoup(r.text, 'lxml')
            links = soup.find_all('a', {'target': '_self'})
            links_all = ['https://www.etm.ru' + i.get('href') for i in links]
            st.write('last - ', int(round((len(links_all) - 5) / 2, 0)))
            for l in links_all[:int(round((len(links_all) - 5) / 2, 0))]:
                st.write('Now - ', l, 'for goods - ', goods)
                res = requests.get(l, headers=headers)
                time.sleep(1.5)
                soup = BeautifulSoup(res.text, 'lxml')
                try:
                    first_pattern = soup.find('h1').text
                    second_patter = soup.find('p', {'class', 'jss86'}).text
                except Exception as ex:
                    st.write(ex)
                    st.write(l)
                if goods in first_pattern or goods in second_patter:
                    st.write('Yes price for -', goods)
                    try:
                        price = soup.find(text=re.compile('Ваша цена')).find_next('p').text.replace('₽', '').replace(
                            ',',
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
        except Exception as ex:
            st.write(ex)
            browser.quit()
            pass

    browser.quit()
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
    st.write('Excel done')
    with open(f'Парсинг цен - {now_date}.xlsx', "rb") as file:
        st.download_button(
            label="Download data as EXCEL",
            data=file,
            file_name=f'Парсинг цен - {now_date}.xlsx',
            mime='text/xlsx',
        )

if __name__=='__main__':
    st.title('Парсинг цен')
    st.subheader("Контейнер для загрузки Excel")
    uploadedFile = st.file_uploader("Загрузите txt file", type=['csv', 'xlsx'], accept_multiple_files=False,
                                    key="fileUploader")
    if uploadedFile is not None:
        df = pd.read_excel(uploadedFile)
        if len(df.columns) > 10:
            st.write('The second type of docs - ')
            df.set_index('Unnamed: 0', inplace=True)
            df = df.loc['№ П/П':]
            headers = df.iloc[0].tolist()
            df.columns = headers
            df.drop(axis=0, index='№ П/П', inplace=True)
            s_all_final = df['Наименование строительного ресурса, затрат'].tolist()
            s_all_final = s_all_final[1:]
            s_all_final = list(map(lambda x: x if type(x) == str else None, s_all_final))
            s_all_final = list(filter(None, s_all_final))
            s_all_final = list(dict.fromkeys(s_all_final))
            scrapping_avarage_price(s_all_final)

        if 'Ед.' in df.columns:
            st.write('The first type of docs')
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
            scrapping_avarage_price(s_all_final)
        if 'Ед.' not in df.columns:
            st.write('The third type of docs from cloud')
            df = pd.read_excel(uploadedFile, skiprows=2)
            df = df.dropna(subset=['Сметная цена с НДС ', 'Закупочная цена с НДС '])
            del df['№']
            df = df.reset_index()
            del df['index']
            name = df['Артикул'].tolist()
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
            df_new = df[['Сметная цена с НДС ', 'Закупочная цена с НДС ']]
            df_new['Артикул'] = s_all_final
            df_new = df_new.rename(columns={'Сметная цена с НДС ': 'Среднее значение по сметной цене с НДС',
                                            'Закупочная цена с НДС ': 'Среднее значение по закупочной цене с НДС'})
            trial = df_new.groupby('Артикул').mean()
            trial.index.name = 'Название товара'
            now_date = datetime.datetime.now().strftime('%Y-%m-%d')
            writer = pd.ExcelWriter(f'Парсинг цен - {now_date}.xlsx')
            trial.to_excel(writer, index=True)
            writer.save()
            st.write('CSV done')
            with open(f'Парсинг цен - {now_date}.xlsx', "rb") as file:
                st.download_button(
                    label="Download data as CSV",
                    data=file,
                    file_name=f'Парсинг цен - {now_date}.xlsx',
                    mime='text/xlsx',
                )






















# import requests
# from bs4 import BeautifulSoup
# import time
# import streamlit as st
# import csv
# import pandas as pd
# import re
# import lxml
# import re
# from lxml import html
# import datetime
# import selenium
# from shutil import which
# import os, sys
# import numpy as np
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import json
# firefoxOptions = Options()
# FIREFOXPATH = which("firefox")
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
# firefoxOptions.add_argument(f'user-agent={user_agent}')
# firefoxOptions.add_argument('--headless')
# firefoxOptions.add_argument('--no-sandbox')
# firefoxOptions.add_argument("--window-size=1920,1080")
# firefoxOptions.add_argument('--disable-dev-shm-usage')
# firefoxOptions.add_argument('--ignore-certificate-errors')
# firefoxOptions.add_argument('--allow-running-insecure-content')
# firefoxOptions.binary = FIREFOXPATH

# path = os.getcwd()
# st.write(path)

# @st.experimental_singleton
# def installff():
#   os.system('sbase install geckodriver')
#   os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver.exe')

# _ = installff()

# st.title('Парсинг цен')
# st.subheader("Контейнер для загрузки Excel")
# uploadedFile = st.file_uploader("Загрузите txt file",  type=['csv','xlsx'],accept_multiple_files=False,key="fileUploader")
# if uploadedFile is not None:
#     df = pd.read_excel(uploadedFile)
#     if len(df.columns) > 10:
#         st.write('The second type of docs - ')
#         df.set_index('Unnamed: 0', inplace = True)
#         df = df.loc['№ П/П':]
#         headers = df.iloc[0].tolist()
#         df.columns = headers
#         df.drop(axis = 0, index = '№ П/П', inplace = True)
#         s_all_final = df['Наименование строительного ресурса, затрат'].tolist()
#         s_all_final = s_all_final[1:]
#         s_all_final = list(map(lambda x: x if type(x) == str else None, s_all_final))
#         s_all_final = list(filter(None, s_all_final))
#         s_all_final = list(dict.fromkeys(s_all_final))

#     if 'Ед.' in df.columns:
#         st.write('The first type of docs')
#         name = df['Артикул, марка '].tolist()
#         articl = df['Наименование'].tolist()
#         all_name = [[i, j] for i, j in zip(articl, name)]
#         s_all = []
#         for i in range (len(all_name)):
#             if type(all_name[i][1]) == str:
#                 s_all.append(all_name[i][1])
#             elif all_name[i][1] is np.nan:
#                 all_name[i][1] = all_name[i][0]
#                 s_all.append(str(all_name[i][1]))
#         s_all_final = []
#         for i in s_all:
#             if i == 'nan':
#                 continue
#             else:
#                 s_all_final.append(i)
#         s_all_final = list(map(lambda x: x.replace('\n', ''), s_all_final))
#     if 'Ед.' not in df.columns:
#         st.write('The third type of docs from cloud')
#         df = pd.read_excel(uploadedFile, skiprows=2)
#         df = df.dropna(subset=['Сметная цена с НДС ', 'Закупочная цена с НДС '])
#         del df['№']
#         df = df.reset_index()
#         del df['index']
#         name = df['Артикул'].tolist()
#         articl = df['Наименование'].tolist()
#         all_name = [[i, j] for i, j in zip(articl, name)]
#         s_all = []
#         for i in range (len(all_name)):
#             if type(all_name[i][1]) == str:
#                 s_all.append(all_name[i][1])
#             elif all_name[i][1] is np.nan:
#                 all_name[i][1] = all_name[i][0]
#                 s_all.append(str(all_name[i][1]))
#         s_all_final = []
#         for i in s_all:
#             if i == 'nan':
#                 continue
#             else:
#                 s_all_final.append(i)
#         s_all_final = list(map(lambda x: x.replace('\n', ''), s_all_final))
#         df_new = df[['Сметная цена с НДС ', 'Закупочная цена с НДС ']]
#         df_new['Артикул'] = s_all_final
#         df_new = df_new.rename(columns={'Сметная цена с НДС ':'Среднее значение по сметной цене с НДС','Закупочная цена с НДС ':'Среднее значение по закупочной цене с НДС'})
#         trial = df_new.groupby('Артикул').mean()
#         trial.index.name = 'Название товара'
#         now_date = datetime.datetime.now().strftime('%Y-%m-%d')
#         writer = pd.ExcelWriter(f'Парсинг цен - {now_date}.xlsx')
#         trial.to_excel(writer, index=True)
#         writer.save()
#         st.write('CSV done')
#         with open(f'Парсинг цен - {now_date}.xlsx', "rb") as file:
#             st.download_button(
#                 label="Download data as CSV",
#                 data=file,
#                 file_name=f'Парсинг цен - {now_date}.xlsx',
#                 mime='text/xlsx',
#             )
        
         
     
    
    
    
#     st.write('Begin scrapping')
#     good_links = {}
#     browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options = firefoxOptions)
#     for goods in s_all_final:
#       good_links[goods] = []
#       try:
#           # THE FIRST SITE
#           url_1 = f'https://www.tinko.ru/search?q={goods}'
#           res = requests.get(url_1)
#           time.sleep(1.5)
#           soup = BeautifulSoup(res.text, 'lxml')
#           links = soup.find_all('p', {'class', 'catalog-product__title'})
#           links_ = [i.find('a') for i in links]
#           links_all = ['https://www.tinko.ru' + i.get('href') for i in links_]
#           for l in links_all[:int(round((len(s_all_final) -5) /2, 0))]:
#               st.write('Now - ', l, 'for goods - ', goods)
#               r = requests.get(l)
#               time.sleep(1.5)
#               soup = BeautifulSoup(r.text, 'lxml')
#               try:
#                   first_pattern = soup.find('h1').text
#                   second_pattern = soup.find('h2').text
#               except Exception as ex:
#                   st.write(ex)
#                   st.write(l)
#               if goods in first_pattern or goods in second_pattern:
#                   st.write('Yes price')
#                   try:
#                       price = soup.find('span', {'class', 'product-detail__price-value'}).text.replace(' ', '').replace(
#                           ',', '.')
#                       st.write(price, 'for site - ', goods)
#                       good_links[goods].append(price)
#                       break
#                   except Exception as ex:
#                       st.write(ex)
#                       st.write(l)
#                       break
#               else:
#                   continue
#           # THE SECOND SITE
#           url_2 = f"https://videoglaz.ru/?digiSearch=true&term={goods}&params=%7Csort%3DDEFAULT"
#           #         browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options = firefoxOptions)
#           browser.implicitly_wait(7)
#           browser.get(url_2)
#           time.sleep(5)
#           html = browser.page_source
#           soup_ = BeautifulSoup(html, 'lxml')
#           links = soup_.find_all('div', {'class': 'digi-product'})
#           links_ = [i.find('a') for i in links]
#           links_all = ['https://videoglaz.ru' + i.get('href') for i in links_]
#           for l in links_all[:int(round((len(s_all_final) -5) /2, 0))]:
#               st.write('Now - ', l, 'for goods - ', goods)
#               res = requests.get(l)
#               time.sleep(1.5)
#               soup = BeautifulSoup(res.text, 'lxml')
#               try:
#                   first_pattern = soup.find('h1', {'class': 'm-0 good-title'}).text
#                   second_pattern = soup.find('div', {'class': 'tab-content m-3'}).text
#               except Exception as ex:
#                   st.write(ex)
#                   st.write(l)
#               if goods in first_pattern or goods in second_pattern:
#                   st.write('Yes price')
#                   try:
#                       price = soup.find('div', {'class': 'cenaWrap'}).find('b').text.replace(' ', '').replace(',', '.')
#                       st.write(price, 'for site - ', goods)
#                       good_links[goods].append(price)
#                       break
#                   except Exception as ex:
#                       st.write(ex)
#                       st.write(l)
#                       break
#               else:
#                   continue
#                   # THE THIRD SITE
#           url_3 = f'https://www.citilink.ru/search/?text={goods}'
#           #         browser = webdriver.Firefox(executable_path=r'/home/appuser/venv/bin/geckodriver.exe', options = firefoxOptions)
#           browser.implicitly_wait(2)
#           browser.get(url_3)
#           time.sleep(3)
#           browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#           time.sleep(2)
#           html = browser.page_source
#           soup = BeautifulSoup(html, 'lxml')
#           links = soup.find_all('a', {'class': 'ProductCardVertical__name Link js--Link Link_type_default'})
#           links_all = ['https://www.citilink.ru' + i.get('href') for i in links]
#           for l in links_all[:5]:
#               st.write('Now - ', l, 'for goods - ', goods)
#               browser.get(l)
#               time.sleep(2)
#               html = browser.page_source
#               time.sleep(2)
#               soup = BeautifulSoup(html, 'lxml')
#               try:
#                   first_pattern = soup.find('h1').text
#               except Exception as ex:
#                   st.write(ex)
#                   st.write(l)
#               if goods in first_pattern:
#                   try:
#                       price = soup.find('span', {
#                           'class': "ProductPrice__price ProductCartFixedBlockNEW__price__price"}).text.replace('\n',
#                                                                                                                '').replace(
#                           '₽', '').replace(' ', '').replace(',', '.').strip()
#                       st.write(price, 'for site - ', goods)
#                       good_links[goods].append(price)
#                       break
#                   except Exception as ex:
#                       st.write(ex)
#                       st.write(l)
#                       break
#               else:
#                   continue

#           # THE FORTH SITE
#           url_4 = f'https://sort.diginetica.net/search?st={goods}&apiKey=D1K76714Q4&strategy=vectors_extended,zero_queries_predictor&fullData=true&withCorrection=true&withFacets=true&treeFacets=true&regionId=global&useCategoryPrediction=true&size=20&offset=0&showUnavailable=true&unavailableMultiplier=0.2&preview=false&withSku=false&sort=DEFAULT'
#           res = requests.get(url_4)
#           time.sleep(2)
#           res = res.text
#           js = json.loads(res)
#           js = js['products']
#           for good in js:
#               name = good['name']
#               if goods in name:
#                   price = good['price']
#                   st.write(price, 'for site - ', goods)
#                   good_links[goods].append(price)
#                   break

#           # THE FIFTH SITE
#           headers = {
#               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.'}
#           url_5 = f'https://www.etm.ru/catalog?searchValue={goods}&rows=12'
#           r = requests.get(url_5, headers=headers)
#           time.sleep(1.5)
#           soup = BeautifulSoup(r.text, 'lxml')
#           links = soup.find_all('a', {'target': '_self'})
#           links_all = ['https://www.etm.ru' + i.get('href') for i in links]
#           for l in links_all[:int(round((len(s_all_final) -5) /2, 0))]:
#               st.write('Now - ', l, 'for goods - ', goods)
#               res = requests.get(l, headers=headers)
#               time.sleep(1.5)
#               soup = BeautifulSoup(res.text, 'lxml')
#               try:
#                   first_pattern = soup.find('h1').text
#                   second_patter = soup.find('p', {'class', 'jss86'}).text
#               except Exception as ex:
#                   st.write(ex)
#                   st.write(l)
#               if goods in first_pattern or goods in second_patter:
#                   st.write('Yes price for -', goods)
#                   try:
#                       price = soup.find(text=re.compile('Ваша цена')).find_next('p').text.replace('₽', '').replace(',',
#                                                                                                                    '.').replace(
#                           ' ', '')
#                       st.write(price, 'for site - ', l)
#                       good_links[goods].append(price)
#                       break
#                   except Exception as ex:
#                       st.write(ex)
#                       st.write(l)
#                       break
#               else:
#                   continue
#       except Exception as ex:
#           st.write(ex)
#           browser.quit()
#           pass
                
#     browser.quit()
#     dict_2 = {}
#     for k, v in good_links.items():
#         flot_no = list(filter(None, v))
#         if len(flot_no) > 0:
#             len_ = len(flot_no)
#             list_ = list(map(float, flot_no))
#             sum_ = sum(list_)
#             avarage = sum_ / len_
#             dict_2[k] = avarage

#     df = pd.DataFrame.from_dict(dict_2, orient='index', columns=['Средняя цена товара'])
#     df.index.name = 'Название товара'
#     now_date = datetime.datetime.now().strftime('%Y-%m-%d')
#     writer = pd.ExcelWriter(f'Парсинг цен - {now_date}.xlsx')
#     df.to_excel(writer, index=True)
#     writer.save()

#     st.write('CSV done')

#     with open(f'Парсинг цен - {now_date}.xlsx', "rb") as file:
#         st.download_button(
#             label="Download data as CSV",
#             data=file,
#             file_name=f'Парсинг цен - {now_date}.xlsx',
#             mime='text/xlsx',
#         )







