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

# List of important financial, technological or cryptocurrency centres
places = ['New York', 'San Francisco', 'London', 'Singapore', 'Toronto', 'Hong Kong', 'Zurich', 'Berlin', 'Tokyo', 'Seoul', 'Shanghai', 'Dubai', 'Bangalore', 'Tel Aviv', 'Amsterdam', 'Sydney', 'Sao Paulo', 'Moscow', 'Paris', 'Los Angeles', 'Chicago']

# Loop over places
for place in places:
    # List of key terms in the cryptocurrency and blockchain industry
    hashtags = ['Bitcoin', 'Ethereum', 'Blockchain', 'Cryptocurrency', 'Crypto', 'BTC', 'ETH', 'DeFi', 'CryptoTrading', 'HODL', 'Altcoin', 'CryptoNews', 'Cryptowallet', 'BitcoinMining', 'BitcoinPrice', 'EthereumPrice', 'SmartContract', 'NFT', 'Stablecoin', 'DApp', 'ICO', 'TokenSale', 'Binance', 'Coinbase', 'Ripple', 'XRP', 'Litecoin', 'Dogecoin']

    # Initialize WebDriver with path to GeckoDriver
    driver = webdriver.Firefox(executable_path= r'') #Your GeckoDriver Path

    # Navigate to Google
    driver.get("https://www.google.com")

    # Loop over hashtags
    for tag in hashtags:
        # List to store the results
        results = []
        # Find the search box on the page
        search = driver.find_element(by=By.CSS_SELECTOR, value="textarea.gLFyf")
        
        # Generate query programmatically 
        query = place + ' '  + tag + ' \"@gmail.com\" '
        # Clear the search box and enter the query
        search.clear()
        search.send_keys(query)

        # Submit the search
        search.send_keys(Keys.RETURN)

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Check for recaptcha
        div_element = soup.find("div", id="recaptcha")
        if div_element:
            # If recaptcha is found, wait for 30 seconds
            time.sleep(30)

        # Wait for the page to load
        time.sleep(random.randint(3,5))

        # Regular expression to search in the span
        regex = r'[a-zA-Z0-9_.+-]+@gmail\.com'

        try:
            # Loop over the first 100 pages of results
            for _ in range(100):
                # Parse the page with BeautifulSoup
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Check for recaptcha
                div_element = soup.find("div", id="recaptcha")
                if div_element:
                    # If recaptcha is found, wait for 30 seconds
                    time.sleep(30)

                # Find all span elements
                spans = soup.find_all('span')

                # For each span, find the text that matches the regex
                for span in spans:
                    matches = re.findall(regex, span.text)
                    results.extend(matches)
                
                # Create a DataFrame with the results
                df = pd.DataFrame(results)
                # Append to the csv file
                df.to_csv('results-IG-01', index=False, mode="a", header=False)

                # Go to the next page
                try:
                    next_page = driver.find_element(by=By.XPATH, value="//span[text()='Siguiente']")     
                    next_page.click()
                except:
                    print("No more pages")
                    break

                # Wait for the page to load
                time.sleep(random.randint(1,3))
        except NoSuchElementException:
            # No results found for this search, continue to the next
            print(f"No results found for the search: {query}")
            continue

    # Close the driver
    driver.quit()

    # Random delay before the next iteration
    time.sleep(random.randint(5,8))
