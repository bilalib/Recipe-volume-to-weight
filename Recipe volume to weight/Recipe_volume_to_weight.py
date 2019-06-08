from Recipe import *
import os

link = "https://www.justonecookbook.com/souffle-pancake/#wprm-recipe-container-69708"
s = Scraper(link)
s.auto_scrape()
print(s.recipe_to_string())