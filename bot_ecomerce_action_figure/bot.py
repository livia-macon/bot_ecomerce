from botcity.web import WebBot, Browser
from botcity.web.browsers.chrome import default_options
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import requests
from base_bot import BotEcomerce

class Bot(WebBot):

    def action(self, execution=None):

        # Parameter search
        self.search = BotEcomerce("action figure Yoda", "Yoda", "32789")

        # open browse
        self.search.generate_link()

        # Choice country
        self.search.choice_country()
        # Input zip_code
        self.search.input_zipcode()

        #extract price and shipping
        self.search.extract_price_shipping()

        # create plan with data extract
        self.search.create_plan()


if __name__ == '__main__':
    Bot.main()
