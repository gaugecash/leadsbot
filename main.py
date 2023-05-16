import random
from time import sleep
from pyppeteer import launch
from pyppeteer_stealth import stealth 
import re
import asyncio
import csv

def extract_emails(html_content):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, html_content)
    return emails

def clean_emails(emails):
    clean_emails = []
    for i in range(len(emails)):
        clean = emails[i].replace('%3D', '').replace('%2522','').replace('q%3D', '').replace('%2B', '').replace('%22', '').replace('+', '').replace('x22', '').replace('x3d', '')
        clean_emails.append(clean)
    return clean_emails

def write_emails_to_csv(input):
    with open('emails.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for email in input:
            writer.writerow([email])

user_agents = [    
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',    
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.3',   
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',    
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.55',    
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',    
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',    
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',    
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',    
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',    
    # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    ]


# List of proxies to rotate IP addresses
proxies = [
    'http://10.10.1.10:3128',
    'https://10.10.1.11:1080',
    'https://192.168.1.1:8080',
    'http://192.168.1.1:8080',
    # 'http://138.197.157.44:3128',
    # 'http://138.197.157.32:3128',
    # 'http://178.62.193.19:3128',
    # 'http://138.68.60.8:3128',
    # 'http://35.176.146.182:80',
    # 'http://35.178.5.145:8080',
    # 'http://35.178.117.107:80',
    # 'http://157.230.44.220:3128',
    # 'http://207.154.231.213:3128'
]
#hashtags = ['bitcoin', 'cryptocurrencies', 'ethereum', 'altcoins', 'blockchain', 'decentralization', 'cryptoexchange', 'cryptomining', 'smartcontracts', 'digitalcurrency', 'cryptowallet', 'cryptonews', 'hodl', 'coinbase', 'binance', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'defi']
#places = [ 'new jersey', 'boston', ]#'chicago',   'New York',    'Los Angeles',    'Chicago',    'San Francisco',    'Toronto',    'Paris',    'London',    'Amsterdam',    'Dublin',    'Sydney',    'Melbourne',    'Tokyo',    'Osaka',    'Seoul',    'Berlin',    'Hamburg',    'Vienna',    'Zurich',    'Stockholm',    'Copenhagen']

places = [ 'new jersey', 'boston', ]# 'chicago',   'New York',   'Los Angeles',    'Chicago',    'San Francisco',    'Toronto',    'Paris',    'London',    'Amsterdam',    'Dublin',    'Sydney',    'Melbourne',    'Tokyo',    'Osaka',    'Seoul',    'Berlin',    'Hamburg',    'Vienna',    'Zurich',    'Stockholm',    'Copenhagen']

hashtags = [ 'smartcontracts', 'digitalcurrency', 'cryptowallet', 'cryptonews', 'hodl', 'coinbase', 'binance', 'bitcoincash', 'dogecoin', 'litecoin', 'staking', 'defi']
leads = []

async def scrape_query(query):
    url = f"https://www.google.com/search?q={query}"
    
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    
    # Use Puppeteer Stealth to prevent detection
    await stealth(page)

    # Select a random user-agent and proxy for each request
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    proxy = random.choice(proxies)

    # Set the user-agent and proxy
    await page.setUserAgent(headers['User-Agent'])
    await page.authenticate({'proxy': proxy})
    
    # Navigate to the search page and wait for the results to load
    await page.goto(url)
    await page.waitForSelector('#search')
        
    # Extract the HTML content of the search results
    html_content = await page.content()

    # Extract the emails from the HTML content
    emails = extract_emails(html_content)
    emails = clean_emails(emails)
    leads.extend(emails)
    
    await browser.close()

async def main():
    tasks = []
    for place in places:
        for hashtag in hashtags:
            query = place + ' ' + hashtag + ' \"@gmail.com\" site:instagram.com'
            task = asyncio.create_task(scrape_query(query))
            tasks.append(task)
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        write_emails_to_csv(leads)
    #print(leads)

if __name__ == '__main__':
    asyncio.run(main())
