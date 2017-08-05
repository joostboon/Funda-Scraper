## Basic tool for (gently) scraping property listings from Dutch housing site [Funda.nl](http://www.funda.nl), written in Python using Selenium.

Please note:

- scraping this website is only allowed for personal use (as per Funda's Terms and Conditions).
- funda.nl seems to use the anti-scraping services of Distil Networks so when running this scraper you will have to manually pass a Captcha every now and then
- this tool is structured in a such a way that it gently / ethically scrapes the pages it encounters (in other words, scraping data will take a while given the numerous "sleep" intervals embedded in the code)
- you will have to point the init_browser function to the local path of your webdriver (through the file_path variable)

The code takes as input search terms that would normally be entered on the Funda home page. It extracts 7 variables from each property listing, which in turn is appended to a dataframe and saved to a CSV file.
It further takes the number of pages you would like to extract as an input (nb - each pararius results page contains 15 listings).

This tool was written by means of [Python 3.5.1](https://www.python.org/downloads/release/python-351/), [Selenium 3.4.3](https://pypi.python.org/pypi/selenium) and [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/).

NB - inside the custom_page folder you will find a scraper that allows to scrape custom page ranges (instead of the base scraper that as a standard starts at page 1)

Example of the resulting dataframe:

```
      city     link                                               price
0   Amsterdam  http://www.funda.nl/koop/amsterdam/appartement...  497500
1   Amsterdam  http://www.funda.nl/koop/amsterdam/huis-858086...  685000
2   Amsterdam  http://www.funda.nl/koop/amsterdam/huis-856042...  220000
3   Amsterdam  http://www.funda.nl/koop/amsterdam/huis-852283...  232500
4   Amsterdam  http://www.funda.nl/koop/amsterdam/huis-858792...  300000
5   Amsterdam  http://www.funda.nl/koop/amsterdam/appartement...  425000

        rooms                               street_zipcode_city   surface
0          4                    Oeverpad 508\n1068 PM Amsterdam     171
1    / 396 5                    Hoekenes 106\n1068 NA Amsterdam     185
2    / 123 4           Hendrik Godfroidhof 3\n1106 WS Amsterdam      71
3    / 108 3             Anne Kooistrahof 21\n1106 WG Amsterdam      90
4     / 99 4              Grootslagstraat 29\n1024 EZ Amsterdam      90
5          3              Marnixstraat 313 c\n1016 TB Amsterdam      73

    zipcode
0   1068 PM
1   1068 NA
2   1106 WS
3   1106 WG
4   1024 EZ
5   1016 TB
```

#### Output mapped in Tableau for the city of Amsterdam (price / square meters of surface)
![alt text](https://raw.githubusercontent.com/Weesper1985/Funda-Scraper/master/Sheet.png)
