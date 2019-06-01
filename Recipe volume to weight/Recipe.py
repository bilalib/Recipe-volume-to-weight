import requests
from lxml import html
from Ingredient_measurements import *


class Recipe(object):
    def __init__(self):
        conversions = Ingredient_measurements()

    def getIngList(self, link):
        with requests.get(link) as page:    
            tree = html.fromstring(page.content)
        ingredients = tree.xpath('//*[@id="lst_ingredients_1"]/li/label/span/text()')
        return ingredients

    def parseIngList(self, ingredients):
        def fracToFloat(frac):
            if '/' in frac:
                frac = frac.split('/')
                return int(frac[0]) / int(frac[1])
            else:
                return frac

        for i in range(len(ingredients)):
            ingredients[i] = temp = ingredients[i].split(' ', 2)
            ingredients[i][0] = fracToFloat(temp[0])

        return ingredients
