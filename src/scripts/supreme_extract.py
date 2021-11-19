import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

baseUrl = "https://www.supremenewyork.com/shop/all/tops_sweaters"



r = requests.get(baseUrl)
soup = bs(r.content, 'html.parser')
names = soup.select('div.product-name')
styles = soup.select('div.product-style')

links = [baseUrl + x.find('a')["href"] for x in soup.select('div.inner-article')]

for name, style, link in zip(names, styles, links):
    print(f"Name: {name.text}, Style: {style.text}, Link: {link}")

def open_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, executable_path='/users/kkubo/Downloads/chromedriver')
    driver.get(baseUrl)

    # driver.find_element_by_id('Glitter').click()
    driver.find_element_by_link_text('Glitter S/S Top').click()

# open_browser()



