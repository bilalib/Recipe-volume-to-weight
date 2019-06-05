import requests
from lxml import html
from lxml import etree

class Scraper(object):
    
    wprm_sites = {"jocooks", "justonecookbook"}

    def __init__(self, link):
        self.ings = list()
        with requests.get(link) as page:
            self.tree = html.fromstring(page.content)

        # wprm works for all sites that use wordpress recipe maker
        if any(site in link for site in Scraper.wprm_sites):
            self.wprm()
        if "allrecipes" in link:
            self.allrecipes()

    def allrecipes(self):
        path = '//span[@class="recipe-ingred_txt added"]/text()'
        self.ings = self.tree.xpath(path)

    def wprm(self):
        path = '//li[contains(@class, "wprm-recipe-ingredient")]'
        self.ings = [str(x.text_content()) for x in self.tree.xpath(path)]
        # Removes leading spaces from each ingredient
        for i, _ in enumerate(self.ings):
            while self.ings[i][0] == " ":
                self.ings[i] = self.ings[i][1:]