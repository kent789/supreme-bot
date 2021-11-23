import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import helpers

class supremeBot(object):
    def __init__(self, **info):
        self.base_url = 'https://www.supremenewyork.com/'
        self.shop = 'shop/all/'
        self.checkout = 'checkout/'
        self.info = info

    def findProduct(self):
        try:
            productPage = requests.get(
                "{}{}{}".format(
                    self.base_url,
                    self.shop,
                    self.info['category']))
            soup = bs(productPage.content, 'html.parser')

            names = soup.select('div.product-name')
            styles = soup.select('div.product-style')

            links = [productPage.url + x.find('a')["href"] for x in soup.select('div.inner-article')]

            for name, style, link in zip(names, styles, links):
                #print(f"Name: {name.text}, Style: {style.text}, Link: {link}")
                if (name.text == self.info['product'] and style.text == self.info['color'] ):
                    self.final_link = link.replace(productPage.url + '/', '')
                    return True
        except:
            return False

 
 


