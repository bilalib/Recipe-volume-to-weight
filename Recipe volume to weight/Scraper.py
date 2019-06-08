import requests
from lxml import html
import io

class Scraper(object):
    
    wprm_sites = frozenset({"jocooks", "justonecookbook"})

    def __init__(self, link):
        self.link = link
        self.ings = list()
        self.title = str()
        self.dirs = list()
        with requests.get(link) as page:
            self.tree = html.fromstring(page.content)
    
    @staticmethod
    def auto_scrape_ings(link):
        scr = Scraper(link)
        scr.auto_scrape()
        return scr.ings

    def auto_scrape(self):
        # wprm works for all sites that use wordpress recipe maker
        if any(site in self.link for site in Scraper.wprm_sites):
            self.wprm()
        if "allrecipes" in self.link:
            self.allrecipes()
        if "martha" in self.link:
            self.martha()
        if "smitten" in self.link:
            self.smitten()
        if "budgetbytes" in self.link:
            self.budgetbytes()
        if "damndelicious" in self.link:
            self.damndelicious()

    def recipe_to_string(self):
        with io.StringIO() as buffer:
            buffer.write(self.title + "\n\nIngredients\n")
            for ing in self.ings:
                buffer.write(ing + "\n")
            buffer.write("\nDirections\n")
            for dir in self.dirs:
                buffer.write(dir + "\n")
            return buffer.getvalue()
            
    def _get_strip(self, path):
        elt = self.tree.xpath(path)
        return [str(x.text_content()).strip() for x in elt]

    def wprm(self):
        ings_path = '//li[contains(@class, "wprm-recipe-ingredient")]'
        self.ings = self._get_strip(ings_path)
        title_path = '//div[@class="wprm-recipe-name wprm-color-header"]/text()'
        self.title = self.tree.xpath(title_path)[0]
        dirs_path = '//div[@class="wprm-recipe-instruction-text"]/text()'
        self.dirs = self.tree.xpath(dirs_path)

    def allrecipes(self):
        ings_path = '//span[@class="recipe-ingred_txt added"]/text()'
        self.ings = self.tree.xpath(ings_path)
        title_path = '//h1[@class="recipe-summary__h1"]/text()'
        self.title = self.tree.xpath(title_path)[0]
        dirs_path = '//span[@class="recipe-directions__list--item"]'
        self.dirs = self._get_strip(dirs_path)[:-1]

    def martha(self):
        ings_path = '//span[@class="component-text"]'
        self.ings = self._get_strip(ings_path)

    def smitten(self):
        ings_path = '//p[starts-with(text(), "Makes ")]'
        ings_elt = self.tree.xpath(ings_path)[0].getnext()
        self.ings = str(ings_elt.text_content()).split("\n")

    def budgetbytes(self):
        self.wprm()
        # Removes the cost which messes with parsing
        self.ings = [ing.rpartition(" ")[0] for ing in self.ings]

    def damndelicious(self):
        ings_path = '//li[@itemprop="ingredients"]'
        ings_elt = self.tree.xpath(ings_path)
        self.ings = [elt.text_content() for elt in ings_elt]