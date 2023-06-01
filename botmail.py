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
api_key = '045c1fcb49ac4f3d70673df49b51f828'

places = [ "Singapore", "Zug, Switzerland", "Tel Aviv, Israel", "Lagos, Nigeria", 
    "Cheyenne, Wyoming, USA", "London, England", "Berlin, Germany", 
    "Miami, Florida, USA", "San Francisco, California, USA", ]
hashtags = ['coinbase', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'cryptomining', 'Bitcoin', 'Ethereum', 'digitalcurrency', 'Crypto', 'Altcoin', 'cryptowallet', 'cryptonews', 'hodl', 'Cryptocurrency', 'NFT', 'USDT', 'BTC', 'ETH', ' \"BNB\" ','Blockchain', 'Binance', 'Stablecoin','\"DEX\"', 'DigitalAsset']

for place in places:
    driver = webdriver.Firefox()
    driver.get("https://www.google.com")

    for tag in hashtags:
        results = []
        try:
            print('try')
            search = driver.find_element(by=By.CSS_SELECTOR, value="textarea.gLFyf")
            query = place + ' '  + '#' + tag + ' \"@gmail.com\" site:instagram.com'
            search.clear()
            search.send_keys(query)
            search.send_keys(Keys.RETURN)

        except:
            print('except')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            div_element = soup.find("div", class_="g-recaptcha")
            if div_element:
                site_key = soup.find("div", class_="g-recaptcha")['data-sitekey']
                s = f"sitekey: {site_key}"
                print(s)
                data_s = soup.find("div", class_="g-recaptcha")['data-s']
                s = f"data_s: {data_s}"
                print(s)
                site_url = driver.current_url
                url = f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={site_url}&data-s={data_s}"
                print(url)
                response = requests.get(url)
                if response.ok:
                    captcha_id = None

                    try:
                        s = f"response: {response.text}"
                        print(response.text)
                        captcha_id = response.text.split('|')[1]
                        s = f"captcha_id: {captcha_id}"
                        print(s)
                    except:
                        s = f"response: {response.text}"
                        print(s)
                    url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
                    print(url)
                    s = f"Timeout 20 secs"
                    print(s)
                    time.sleep(20) #timeout suggested by  documentation between 15-20 secs
                    while True:
                        res = requests.get(url)
                        if res.ok:
                            if 'CAPCHA_NOT_READY' in res.text:
                                time.sleep(5)
                                continue
                            print(res.text)
                            captcha_answer = res.text.split('|')[1]
                            s = f"captcha_answer: {captcha_answer }"
                            print(s)
                            break

                    driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_answer}';")
                    s = f"click!"
                    print(s)
                    driver.find_element(By.XPATH,  "//span[@role='checkbox']").click()

                    search = driver.find_element(by=By.CSS_SELECTOR, value="textarea.gLFyf")
                    query = place + ' '  + '#' + tag + ' \"@gmail.com\" site:instagram.com'
                    search.clear()
                    search.send_keys(query)
                    search.send_keys(Keys.RETURN)

        time.sleep(random.randint(3,5))

        regex = r'[a-zA-Z0-9_.+-]+@gmail\.com'

        try:
            for _ in range(100):
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                div_element = soup.find("div", class_="g-recaptcha")
                  
                if div_element:
                    site_key = soup.find("div", class_="g-recaptcha")['data-sitekey']
                    s = f"sitekey: {site_key}"
                    print(s)
                    data_s = soup.find("div", class_="g-recaptcha")['data-s']
                    s = f"data_s: {data_s}"
                    print(s)
                    site_url = driver.current_url
                    url = f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={site_url}&data-s={data_s}"
                    response = requests.get(url)
                    if response.ok:
                        captcha_id = response.text.split('|')[1]
                        url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
                        time.sleep(20)
                        while True:
                            res = requests.get(url)
                            if res.ok:
                                if 'CAPCHA_NOT_READY' in res.text:
                                    time.sleep(5)
                                    continue
                                captcha_answer = res.text.split('|')[1]
                                s = f"captcha_answer: {captcha_answer }"
                                print(s)
                                break

                        driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{captcha_answer}';")
                        s = f"click!"
                        print(s)
                        driver.find_element(By.XPATH,  "//span[@role='checkbox']").click()

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
