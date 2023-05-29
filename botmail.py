import os
import requests
import random
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium import webdriver

# Tu clave API de 2captcha
api_key = 'tu_clave_api_de_2captcha'

# Clave del sitio para reCAPTCHA. Necesitarás encontrar esto en el sitio web.
site_key = 'clave_del_sitio_para_reCAPTCHA'
# URL del sitio web que tiene el reCAPTCHA
site_url = 'https://www.example.com'

places = ['Toronto', 'Paris', 'London', 'Amsterdam', 'Dublin', 'Sydney', 'Melbourne', 'Tokyo', 'Osaka', 'Seoul', 'Berlin', 'Hamburg', 'Vienna', 'Zurich', 'Stockholm', 'Copenhagen']
hashtags = ['coinbase', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'cryptomining', 'Bitcoin', 'Ethereum', 'digitalcurrency', 'Crypto', 'Altcoin', 'cryptowallet', 'cryptonews', 'hodl', 'Cryptocurrency', 'DEFI', 'NFT', 'USDT', 'BTC', 'ETH', ' \"BNB\" ','Blockchain', 'Binance', 'Stablecoin','\"DEX\"', 'DigitalAsset']

for place in places:
    driver = webdriver.Firefox(executable_path= r'/Users/j.reuman/Desktop/Dev/GaugeCash/GeckoDriver/geckodriver')
    driver.get("https://www.google.com")

    for tag in hashtags:
        results = []
        search = driver.find_element(by=By.CSS_SELECTOR, value="textarea.gLFyf")
        query = place + ' '  + tag + ' \"@gmail.com\" site:instagram.com'
        search.clear()
        search.send_keys(query)
        search.send_keys(Keys.RETURN)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div_element = soup.find("div", id="recaptcha")
        if div_element:
            url = f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={site_url}&version=v3"
            response = requests.get(url)
            if response.ok:
                captcha_id = response.text.split('|')[1]
                url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
                time.sleep(5)
                while True:
                    res = requests.get(url)
                    if res.ok:
                        if 'CAPCHA_NOT_READY' in res.text:
                            time.sleep(5)
                            continue
                        captcha_answer = res.text.split('|')[1]
                        break

                driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_answer}';")
            time.sleep(30)

        time.sleep(random.randint(3,5))

        regex = r'[a-zA-Z0-9_.+-]+@gmail\.com'

        try:
            for _ in range(100):
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                div_element = soup.find("div", id="recaptcha")
                if div_element:
                    time.sleep(30)

                spans = soup.find_all('span')

                for span in spans:
                    matches = re.findall(regex, span.text)
                    results.extend(matches)

                df = pd.DataFrame(results)
                df.to_csv('results-IG-05-17', index=False, mode="a", header=False)

                try:
                    next_page = driver.find_element(by=By.XPATH, value="//span[text()='Siguiente']")
                    next_page.click()
                except:
                    print("no hay mas paginas")
                    break

                time.sleep(random.randint(1,3))
        except NoSuchElementException:
            print(f"No se encontraron resultados para la búsqueda: {query}")
            continue

    driver.quit()

    time.sleep(random.randint(5,8))
