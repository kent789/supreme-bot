import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import helpers
import time

class SupremeBot(object):
    def __init__(self, **info):
        self.base_url = 'https://www.supremenewyork.com/'
        self.shop = 'shop/all/'
        self.checkout = 'checkout/'
        self.info = info

    def initializeBrowser(self):
        driver = self.info["driver"]
        path = helpers.get_driver_path(driver)
        if driver == "chromedriver":
            executable_path = {"executable_path": path}
            self.b = Browser('chrome', **executable_path)

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

 
    def visitSite(self):
        self.b.visit(
            "{}{}".format(
                self.base_url, 
                self.final_link))
        self.b.find_option_by_text(self.info['size']).click()
        time.sleep(.2) # sleep for 20 milliseconds
        self.b.find_by_value('add to cart').click()

    def checkoutFunc(self):
        time.sleep(.2) # sleep for 20 milliseconds
        self.b.find_by_value('checkout now').click()

        self.b.fill("order[billing_name]", self.info['namefield'])
        self.b.fill("order[email]", self.info['emailfield'])
        self.b.fill("order[tel]", self.info['phonefield'])

        self.b.fill("order[billing_address]", self.info['addressfield'])
        self.b.fill("order[billing_city]", self.info['city'])
        self.b.fill("order[billing_zip]", self.info['zip'])
        self.b.find_option_by_text(self.info['country']).click()

        self.b.fill("credit_card[number]", self.info['number'])

        self.b.find_option_by_text(self.info['month']).click()
        self.b.find_option_by_text(self.info['year']).click()

        self.b.fill("credit_card[verification_value]", self.info['ccv'])
        self.b.find_by_css('.terms').click()

        time.sleep(.2) # sleep for 20 milliseconds
        #self.b.find_by_value("process payment").click()

if __name__ == "__main__":
    INFO = {
        "driver": "chromedriver",
        "product": "Glitter S/S Top",
        "color": "Black",
        "size": "Large",
        "category": "tops_sweaters",
        "namefield": "John Wick",
        "emailfield": "johnWick@gmail.com",
        "phonefield": "(6264543464)",
        "addressfield": "1234 Alison Road",
        "city": "Mountain View",
        "zip": "94040",
        "country": "CA",
        "card": "visa",
        "number": "1234123412341234",
        "month": "09",
        "year": "2023",
        "ccv": "123"
    }

    BOT = SupremeBot(**INFO)
    
    found_product = False 
    max_iter = 5
    counter = 1

    while not found_product and counter < max_iter:
        found_product = BOT.findProduct()
        print(counter, "time try")
        counter += 1
    if not found_product:
        raise Exception("Couldn not find the product")
        
    BOT.initializeBrowser()
    BOT.visitSite()
    #BOT.checkoutFunc()
