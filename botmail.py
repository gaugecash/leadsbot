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

places = ['Toronto', 'Paris', 'London', 'Amsterdam', 'Dublin', 'Sydney', 'Melbourne', 'Tokyo', 'Osaka', 'Seoul', 'Berlin', 'Hamburg', 'Vienna', 'Zurich', 'Stockholm', 'Copenhagen']
#hashtags = ['cryptoexchange', 'cryptomining', 'smartcontracts', 'digitalcurrency', 'cryptowallet', 'cryptonews', 'hodl', 'coinbase', 'binance', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'defi']

# places = ['boston', 'chicago', 'New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Toronto', 'Paris', 'London', 'Amsterdam', 'Dublin', 'Sydney', 'Melbourne', 'Tokyo', 'Osaka', 'Seoul', 'Berlin', 'Hamburg', 'Vienna', 'Zurich', 'Stockholm', 'Copenhagen']

for place in places:
    #hashtags =  ['coinbase', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'cryptomining', 'Bitcoin', 'Ethereum', 'digitalcurrency', 'Crypto', 'Altcoin', 'cryptowallet', 'cryptonews', 'hodl', 'Cryptocurrency', 'DEFI', 'NFT', 'USDT', 'BTC', 'ETH', ' \"BNB\" ','Blockchain', 'Binance', 'Stablecoin','\"DEX\"', 'DigitalAsset']
    hashtags =  ['coinbase', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'cryptomining', 'Bitcoin', 'Ethereum', 'digitalcurrency', 'Crypto', 'Altcoin', 'cryptowallet', 'cryptonews', 'hodl', 'Cryptocurrency', 'DEFI', 'NFT', 'USDT', 'BTC', 'ETH', ' \"BNB\" ','Blockchain', 'Binance', 'Stablecoin','\"DEX\"', 'DigitalAsset']
    driver = webdriver.Firefox(executable_path= r'/Users/j.reuman/Desktop/Dev/GaugeCash/GeckoDriver/geckodriver')

    # Ir a Google
    driver.get("https://www.google.com")

    # Lista para almacenar los resultados
    ##
    for tag in hashtags:
        # Lista para almacenar los resultados
        results = []
        # Encontrar el campo de búsqueda en la página
        #search = driver.find_element_by_css_selector("textarea.gLFyf")
        search = driver.find_element(by=By.CSS_SELECTOR, value="textarea.gLFyf")
        # Entrar el topic a buscar
        #Generar url de manera programatica 
        query = place + ' '  + tag + ' \"@gmail.com\" site:instagram.com'
        search.clear()
        search.send_keys(query)

        # Enviar la búsqueda
        search.send_keys(Keys.RETURN)

        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div_element = soup.find("div", id="recaptcha")
        if div_element:
            time.sleep(30)

        # Esperar a que la página cargue
        # ---- randomizar numero
        time.sleep(random.randint(3,5))

        # Expresión regular para buscar en los span
        regex = r'[a-zA-Z0-9_.+-]+@gmail\.com'

        try:
            # Recorrer las primeras 5 páginas de resultados
            #defnir rango lo suficientemente alto
            for _ in range(100):

                # Parsear la página con BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                div_element = soup.find("div", id="recaptcha")
                if div_element:
                    time.sleep(30)

                # Buscar todos los span
                spans = soup.find_all('span')

                # Por cada span, buscar el texto que coincide con la regex
                for span in spans:
                    matches = re.findall(regex, span.text)
                    results.extend(matches)
                
                # Crear un DataFrame con los resultados
                df = pd.DataFrame(results)
                df.to_csv('results-IG-05-17', index=False, mode="a", header=False)

                # Ir a la siguiente página
                try:
                    next_page = driver.find_element(by=By.XPATH, value="//span[text()='Siguiente']")     
                    next_page.click()
                except:
                    print("no hay mas paginas")
                    break

                # Esperar a que la página cargue
                #---- Elegir valor aleatorio
                time.sleep(random.randint(1,3))
        except NoSuchElementException:
            # No se encontraron resultados para esta búsqueda, pasar a la siguiente
            print(f"No se encontraron resultados para la búsqueda: {query}")
            continue
        

    # Cerrar el driver
    driver.quit()

    time.sleep(random.randint(5,8))
# # Crear un DataFrame con los resultados
# df = pd.DataFrame(results, columns=['Result'])

# # Guardar el DataFrame en un csv
# #Append a la lista
# df.to_csv('results.csv', index=False)