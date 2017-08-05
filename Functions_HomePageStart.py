# Scraper functions, which in turn are sourced in runfile.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import time
from random import randint

# Initialize browser & wait for 15 seconds

def init_browser(filepath):
    browser = webdriver.Chrome(executable_path=filepath)
    browser.implicitly_wait(10)
    return browser

# Open target website

def navigate_to_website(browser):
    browser.get('https://www.funda.nl')

# Wait until site elements are loaded on the home page and enter search term

def enter_search_term(browser, search_term):

    wait = WebDriverWait(browser, 10)

    try:
        search_bar = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='autocomplete-input']")))
        button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='button-primary-alternative']")))
        search_bar.click()
        time.sleep(randint(10, 15))
        search_bar.clear()
        time.sleep(randint(10, 15))
        search_bar.send_keys(search_term)
        time.sleep(randint(10, 15))
        button.click()
        print("search-button has been clicked")
        time.sleep(randint(15, 20))
        return True
    except (TimeoutException, NoSuchElementException) as e:
        print(str(e))
        return False

# Scrape the resulting page and move on to the next page until hitting the predefined lastpage. All results are stored in a csv-file

def get_data(browser, lastpage, search_term):

    data = []

    keep_going = True
    wait = WebDriverWait(browser, 15)
    page = 2

    while keep_going and page <= lastpage:

        try:
            for item in browser.find_elements_by_css_selector("div.search-result-content"):

                try:
                    zipcode1, zipcode2, city = item.find_element_by_css_selector(
                        "small.search-result-subtitle").text.split(" ", 2)
                    zipcode = zipcode1 + " " + zipcode2

                    street_zipcode_city = item.find_element_by_css_selector("h3.search-result-title").text

                    price = item.find_element_by_css_selector("span.search-result-price").text.lstrip('€ ').rstrip(
                        ' k.k,').replace('.', '')

                    surface, rooms = item.find_element_by_css_selector("ul.search-result-kenmerken").text.replace('\n',
                                                                                                                  '').replace(
                        'm²', '').split(" ", 1)
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

            print("page extracted")
            time.sleep(randint(5, 10))

            browser.find_element_by_xpath("//a[contains(@href,'" + search_term + "') and contains(@data-pagination-page,'" + str(page) + "') and contains(@class, 'pagination-number')]").click()
            print("link to page " + str(page) + " has been clicked")
            page += 1
            time.sleep(randint(5, 15))

        except (TimeoutException, NoSuchElementException):
            keep_going = False

    browser.close()
    df = pd.DataFrame(data)
    df.to_csv(search_term+"uptopage"+str(lastpage)+".csv", sep=';', encoding='utf-8')
    print(df)

