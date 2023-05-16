import random
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

places = ['boston', 'chicago', 'New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Toronto', 'Paris', 'London', 'Amsterdam', 'Dublin', 'Sydney', 'Melbourne', 'Tokyo', 'Osaka', 'Seoul', 'Berlin', 'Hamburg', 'Vienna', 'Zurich', 'Stockholm', 'Copenhagen']
hashtags = ['cryptoexchange', 'cryptomining', 'smartcontracts', 'digitalcurrency', 'cryptowallet', 'cryptonews', 'hodl', 'coinbase', 'binance', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'defi']

# Configurar el webdriver para usar Chrome (chromedriver)
driver = webdriver.Firefox()

# Lista para almacenar los resultados
results = []

# Recorrer las combinaciones de lugar y hashtag
for place in places:
    # Reiniciar la lista de resultados para cada lugar
    results.clear()

    for tag in hashtags:
        # Realizar la búsqueda en Google
        query = f'{place} {tag} "@gmail.com" site:instagram.com'
        driver.get(f"https://www.google.com/search?q={query}")

        # Esperar a que la página cargue
        time.sleep(random.randint(1, 3))

        # Expresión regular para buscar en los span
        regex = r'[a-zA-Z0-9_.+-]+@gmail\.com'

        try:
            # Recorrer las páginas de resultados
            while True:
                # Parsear la página con BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Buscar todos los span
                spans = soup.find_all('span')

                # Por cada span, buscar el texto que coincide con la regex
                for span in spans:
                    matches = re.findall(regex, span.text)
                    results.extend(matches)

                # Ir a la siguiente página
                try:
                    next_page = driver.find_element_by_xpath("//span[text()='Siguiente']")
                    next_page.click()

                    # Esperar a que la página cargue
                    time.sleep(random.randint(1, 3))
                except NoSuchElementException:
                    # No hay más páginas, salir del bucle while
                    break

                # Esperar antes de analizar la siguiente página
                time.sleep(random.randint(1, 3))

        except NoSuchElementException:
            # No se encontraron resultados para esta búsqueda, pasar a la siguiente
            print(f"No se encontraron resultados para la búsqueda: {query}")
            continue

        # Crear un DataFrame con los resultados
        df = pd.DataFrame(results, columns=['Result'])

        # Anexar el DataFrame al archivo CSV
        df.to_csv('results2.csv', index=False, mode='a')

# Cerrar el driver
driver.quit()