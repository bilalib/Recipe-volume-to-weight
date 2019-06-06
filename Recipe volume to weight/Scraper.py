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
        if "martha" in link:
            self.martha()
        if "smitten" in link:
            self.smitten()
        if "budgetbytes" in link:
            self.budgetbytes()

    def allrecipes(self):
        path = '//span[@class="recipe-ingred_txt added"]/text()'
        self.ings = self.tree.xpath(path)

    def wprm(self):
        path = '//li[contains(@class, "wprm-recipe-ingredient")]'
        # Removes leading spaces from each ingredient
        self.ings = [str(x.text_content()).strip() 
                     for x in self.tree.xpath(path)]

    def martha(self):
        path = '//span[@class="component-text"]'
        self.ings = self.tree.xpath(path)
        self.ings = [x.text_content().strip() for x in self.ings]

    def smitten(self):
        path = '//p[starts-with(text(), "Makes")]'
        temp = self.tree.xpath(path)[0].getnext()
        self.ings = str(temp.text_content()).split("\n")

    def budgetbytes(self):
        self.wprm()
        # Removes the cost which messes with parsing
        for i, ing in enumerate(self.ings):
            self.ings[i] = ing.rpartition(" ")[0]