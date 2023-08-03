# README

## Description
This Python script performs a series of queries on Google using a combination of locations and cryptocurrency-related hashtags. It then scrapes all Gmail email addresses appearing in the search results and saves them in a CSV file.

## Requirements

### Python Packages
The script requires the following Python packages. You can install them using pip:

- selenium
- pandas
- BeautifulSoup4
- random
- time
- re

To install all necessary packages, you can use the following command:

```shell
pip install selenium pandas beautifulsoup4
```

### GeckoDriver
In addition, you need to have GeckoDriver installed to allow Selenium to control a Firefox browser. You can download it from the [GeckoDriver release page](https://github.com/mozilla/geckodriver/releases). Make sure to download the version that matches your Firefox installation. After downloading, you need to add it to your PATH or change the following line in the script to reflect where you saved it:

```python
driver = webdriver.Firefox(executable_path= r'') ## Add your GeckoDriver path.
```

## How to Run the Script
You can run the script using Python from the command line. Make sure you're in the correct directory containing the script and then use the following command:

```shell
python bot.py
```

## Output
The script will save all found email addresses in a CSV file named "results-IG-01". Each email address will be on a new line. 

## Usage Notes
The script may take a long time to run, as it makes random pauses to avoid being blocked by Google. Also, if it encounters a CAPTCHA, the script will pause for 30 seconds before continuing. If you see the script pausing for a long time, check if Google is asking for a CAPTCHA.

Finally, please note that this script may violate Google's terms of service, and its use may result in your IP being blocked by Google. Additionally, the use of email addresses collected in this way may violate privacy and spam laws, so be sure to use the collected data responsibly and legally.