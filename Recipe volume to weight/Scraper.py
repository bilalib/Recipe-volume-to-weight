import requests
from lxml import html

class Scraper(object):
    
    wprm_sites = frozenset({"jocooks", "justonecookbook"})

    def __init__(self, link):
        self.ings = list()
        with requests.get(link) as page:
            self.tree = html.fromstring(page.content)
    
    @staticmethod
    def auto_scrape(link):
        scr = Scraper(link)
        # wprm works for all sites that use wordpress recipe maker
        if any(site in link for site in Scraper.wprm_sites):
            scr.wprm()
        if "allrecipes" in link:
            scr.allrecipes()
        if "martha" in link:
            scr.martha()
        if "smitten" in link:
            scr.smitten()
        if "budgetbytes" in link:
            scr.budgetbytes()
        return scr.ings
            
    def get_strip(self, path):
        ings_elt = self.tree.xpath(path)
        self.ings = [str(x.text_content()).strip() for x in ings_elt]

    def allrecipes(self):
        path = '//span[@class="recipe-ingred_txt added"]/text()'
        self.ings = self.tree.xpath(path)

    def wprm(self):
        path = '//li[contains(@class, "wprm-recipe-ingredient")]'
        self.get_strip(path)

    def martha(self):
        path = '//span[@class="component-text"]'
        self.get_strip(path)

    def smitten(self):
        path = '//p[starts-with(text(), "Makes ")]'
        ings_elt = self.tree.xpath(path)[0].getnext()
        self.ings = str(ings_elt.text_content()).split("\n")

    def budgetbytes(self):
        self.wprm()
        # Removes the cost which messes with parsing
        self.ings = [ing.rpartition(" ")[0] for ing in self.ings]