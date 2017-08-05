from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
from random import randint

# start your browser

browser = webdriver.Chrome('enter the path to your driver here')

browser.implicitly_wait(15)
wait = WebDriverWait(browser, 30)

# enter the URL you would like to scrape

urls = [
        'http://www.funda.nl/koop/amsterdam/p',
    ]

data = []

# enter the pagerange you would like to scrape

pagerange = range(171, 172)

# start scraping

for url in urls:
    for page in pagerange:
        browser.get(url + str(page))
        # wait for the page to load
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.search-result-content")))

        for item in browser.find_elements_by_css_selector("div.search-result-content"):


            try:
                zipcode1, zipcode2, city = item.find_element_by_css_selector("small.search-result-subtitle").text.split(" ", 2)
                zipcode = zipcode1 + " " + zipcode2

                street_zipcode_city = item.find_element_by_css_selector("h3.search-result-title").text

                price = item.find_element_by_css_selector("span.search-result-price").text.lstrip('€ ').rstrip(
                    ' k.k,').replace('.', '')

                surface, rooms = item.find_element_by_css_selector("ul.search-result-kenmerken").text.replace('\n', '').replace('m²', '').split(" ", 1)
                rooms = rooms.replace('kamer', '').replace('s', '')

                link = item.find_element_by_css_selector("div.search-result-header>a").get_attribute('href')

                data.append({
                    "street_zipcode_city": street_zipcode_city,
                    "zipcode": zipcode,
                    "city": city,
                    "price": price,
                    "surface": surface,
                    "rooms": rooms,
                    "link": link,
                })

            except ValueError:
                pass

        time.sleep(randint(10, 15))

browser.close()
df = pd.DataFrame(data)
df.to_csv("AmsterdamPage"+str(min(pagerange))+"to"+str(max(pagerange))+".csv", sep=';', encoding='utf-8')
print(df)
