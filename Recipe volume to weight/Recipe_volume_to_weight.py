from Ingredient_measurements import *
from Menus import *
import requests
from lxml import html

def getIngredientList(link):
    with requests.get(link) as page:    
        tree = html.fromstring(page.content)
    ingredients = tree.xpath('//*[@id="lst_ingredients_1"]/li/label/span/text()')
    return ingredients

m = Menus()
m.mainMenu()

'''link = ''
ingredients = getIngredientList(link)
measurements = Ingredient_measurements()
for ing in ingredients:
    if ing in measurements.conversions()'''