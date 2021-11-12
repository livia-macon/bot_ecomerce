from botcity.web import WebBot, Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


class BotEcomerce(WebBot):

    def __init__(self, product_search, par_filter, zip_code):
        super().__init__(self)
        self._driver_path = "./chromedriver.exe"
        self._headless = False
        self.product_search = product_search
        self.par_filter = par_filter
        self.zip_code = zip_code

    def generate_link(self):
        self.base_url_ebay = "https://www.ebay.com/"
        self.url_ebay = ("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="
                         + self.product_search.replace(" ", "+")
                         + "&_sacat=0&LH_TitleDesc=0&_odkw=samsung+galaxy+z+fold+3&_osacat=0")

        return self.open_brws(self.url_ebay)

    def open_brws(self, url):
        self.wait(2000)
        self.url = url
        res = requests.get(self.url)

        try:
            if res.status_code == 200:
                print("The server is available, let's the browse.")
                self.browse(self.url)
                self.maximize_window()
        except requests.exceptions.HTTPError as err:

            raise SystemExit(err)

    def choice_country(self):
        # change to USA options
        self.wait(4000)

        if not self.find("usa_choice", matching=0.97, waiting_time=10000):
            self.not_found("usa_choice")
        self.click()

        # self.click()
        self.click()
        self.enter()
        self.wait(4000)

    def input_zipcode(self):

        if not self.find_text("click_ship_to", threshold=230, waiting_time=10000):
            self.not_found("click_ship_to")
        self.click()

        # self.click()
        self.wait(2000)
        self.tab()
        self.tab()
        self.enter()
        self.type_keys('U')
        self.type_down()
        self.type_down()
        self.type_down()
        self.type_down()
        self.enter()
        self.tab()
        self.enter()

        self.wait(4000)

        # input zip code
        if not self.find_text("shipping_click", threshold=230, waiting_time=10000):
            self.not_found("shipping_click")
        self.click()

        # self.click()
        self.tab()
        self.tab()
        self.paste(self.zip_code)
        self.tab()
        self.enter()

    def extract_price_shipping(self):
        # turns the page into an objetc soup
        self.page_source()
        self.soup_ebay = self.page_source()

        # find the box of each product, and its respective product name
        self.product_list_ebay = self.soup_ebay.find_all('div', attrs={'class': 's-item__image'})


        # creat list for store link of each box found previously
        self.list_ebay = []
        self.product_link_ebay = []

        # extract link of each box and append list
        for item in self.product_list_ebay[0:6]:  # self.product_list_bestbuy
            for link in item.find_all('a'):
                self.product_link_ebay.append(link['href'])

        # Open each link extracted, turns the page in an object soup and extract product name, product price and shipping
        for links in self.product_link_ebay:
            self.browse(links)
            self.page_source()
            self.soup_search_ebay = self.page_source()

            self.product_name = self.soup_search_ebay.find('h1', attrs={'class': 'it-ttl'}).text.strip()

            if self.par_filter in self.product_name:

                self.list_ebay.append(self.product_name[15:50])
                self.product_price = self.soup_search_ebay.find('span', attrs={'class': 'notranslate'}).get_text()
                self.list_ebay.append(self.product_price)
                self.product_ship_free = self.soup_search_ebay.find('table', attrs={'class': 'sh-tbl'})
                self.product_ship_free_ = self.product_ship_free.find('td').text.strip()
                self.list_ebay.append(self.product_ship_free_)

            else:
                continue

        self.stop_browser()

        # divide the list into smaller lists with three items
        def list_short(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
            return (lst)

        self.list_df = list(list_short(self.list_ebay, 3))

    def create_plan(self):
        self.plan = pd.DataFrame(self.list_df, columns=["Product", "Price",
                                                        "shipping"])  # index=["Site", "Product", "Price", "shipping"]

        self.plan.to_excel("data_collect_AFigure.xlsx", index=True)
        print(self.plan.head())