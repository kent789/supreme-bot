# import requests
# from bs4 import BeautifulSoup as bs
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://www.supremenewyork.com/shop/all/tops_sweaters"

# r = requests.get(BASE_URL)
# soup = bs(r.content, 'html.parser')
# names = soup.select('div.product-name')
# styles = soup.select('div.product-style')

# links = [BASE_URL + x.find('a')["href"] for x in soup.select('div.inner-article')]

# treasureLink = ''
# shirtTitle = 'Glitter S/S Top'
# shirtColor = 'Black'

# for name, style, link in zip(names, styles, links):
#     #print(f"Name: {name.text}, Style: {style.text}, Link: {link}")
#     if (name.text == shirtTitle and style.text == shirtColor ):
#         treasureLink = link.replace('all/tops_sweaters/shop/', '')

# print(treasureLink)


# # treasureR = requests.get(treasureLink)
# # soup2 = bs(treasureR.content, 'html.parser')
# # print(soup2)


# def open_browser(link):
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)
#     driver = webdriver.Chrome(options=options, executable_path='/users/kkubo/Downloads/chromedriver')
#     driver.get(link)

#     #driver.find_element(By.CSS_SELECTOR, "add to cart").click()
#     #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "add to cart"))).click()

#     driver.find_element_by_link_text('commit').click()
#     #driver.find_element_by_link_text('Glitter S/S Top').click()

# open_browser(treasureLink)

import requests
import bs4 as bs
from splinter import Browser
import helpers


class supremeBot(object):
    def __init__(self, **info):
        self.base_url = 'http://www.supremenewyork.com/'
        self.shop = 'shop/all/'
        self.checkout = 'checkout/'
        self.info = info

    def initializeBrowser(self):
        driver = self.info["driver"]
        #path = helpers.get_driver_path(driver)
        if driver == "geckodriver":
            self.b = Browser()
        elif driver == "chromedriver":
            #executable_path = {"executable_path": path}
            executable_path='/users/kkubo/Downloads/chromedriver'
            self.b = Browser('chrome', executable_path)


    def findProduct(self):
        try:
            # r = requests.get(
            #     "{}{}{}".format(
            #         self.base_url,
            #         self.shop,
            #         self.info['category']))
            #print(r)
            #soup = bs.BeautifulSoup(r, 'html.parser')


            ##########
            

            r = requests.get(BASE_URL)
           
            soup = bs.BeautifulSoup(r.content, 'html.parser')
            names = soup.select('div.product-name')
            styles = soup.select('div.product-style')
            links = [BASE_URL + x.find('a')["href"] for x in soup.select('div.inner-article')]
            for name, style, link in zip(names, styles, links):
                print(f"Name: {name.text}, Style: {style.text}, Link: {link}")
                if (name.text == self.product and style.text == self.color ):
                    treasureLink = link.replace('all/tops_sweaters/shop/', '')
            ########
            print(treasureLink)

            # temp_tuple = []
            # temp_link = []

            # for link in soup.find_all('a', href=True):
            #     temp_tuple.append((link['href'], link.text))

            # print(temp_tuple)

            # for i in temp_tuple:
            #     if i[1] == self.info['product'] or i[1] == self.info['color']:
            #         temp_link.append(i[0])
            
            # self.final_link = list(
            #     set([x for x in temp_link if temp_link.count(x) == 2]))[0]
            return True
        except:
            return False

    def visitSite(self):
        self.b.visit(
            "{}{}".format(
                self.base_url, str(
                    self.final_link)))
        # self.b.visit("https://www.supremenewyork.com/shop/tops-sweaters/b9od7hzwr/bevru9s4n")
        self.b.find_option_by_text(self.info['size']).click()
        self.b.find_by_value('add to basket').click()

    def checkoutFunc(self):

        self.b.visit("{}{}".format(self.base_url, self.checkout))

        self.b.fill("order[billing_name]", self.info['namefield'])
        self.b.fill("order[email]", self.info['emailfield'])
        self.b.fill("order[tel]", self.info['phonefield'])

        self.b.fill("order[billing_address]", self.info['addressfield'])
        self.b.fill("order[billing_city]", self.info['city'])
        self.b.fill("order[billing_zip]", self.info['zip'])
        self.b.select("order[billing_country]", self.info['country'])

        self.b.select("credit_card[type]", self.info['card'])
        self.b.fill("credit_card[cnb]", self.info['number'])
        self.b.select("credit_card[month]", self.info['month'])
        self.b.select("credit_card[year]", self.info['year'])
        self.b.fill("credit_card[ovv]", self.info['ccv'])
        self.b.find_by_css('.terms').click()
        #self.b.find_by_value("process payment").click()


if __name__ == "__main__":
    INFO = {
        "driver": "chromedriver",
        "product": "Glitter S/S Top",
        "color": "Black",
        "size": "Medium",
        "category": "tops_sweaters",
        "namefield": "example",
        "emailfield": "example@example.com",
        "phonefield": "XXXXXXXXXX",
        "addressfield": "example road",
        "city": "example",
        "zip": "72046",
        "country": "GB",
        "card": "visa",
        "number": "1234123412341234",
        "month": "09",
        "year": "2020",
        "ccv": "123"
    }
    BOT = supremeBot(**INFO)
    # Flag to set to true if you want to reload the page continously close to drop.
    found_product = False
    max_iter = 2
    counter = 1
    while not found_product and counter < max_iter:
        found_product = BOT.findProduct()
        print("Tried ", counter, " times")
        counter += 1
    if not found_product:
        raise Exception("Couldn't find product. Sry bruh")
    # BOT.initializeBrowser()
    # BOT.visitSite()
    #BOT.checkoutFunc()

