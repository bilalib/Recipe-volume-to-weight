import requests
from lxml import html
from Ingredient_measurements import *
import openpyxl


class Recipe(object):
    conversions = Ingredient_measurements()

    def __init__(self, ingredients):
        Recipe.ingredients = ingredients
        Recipe.parseIngList(self)

    @classmethod
    def fromLink(self, link):
        return self(Recipe.ingsFromLink(self, link))

    def ingsFromLink(self, link):
        with requests.get(link) as page:    
            tree = html.fromstring(page.content)
        return tree.xpath('//*[@id="lst_ingredients_1"]/li/label/span/text()')

    def parseIngList(self):
        def fracToFloat(frac):
            if '/' in frac:
                frac = frac.split('/')
                return float(frac[0]) / float(frac[1])
            else:
                return frac
        
        for i in range(len(Recipe.ingredients)):
            # Splits the list at first two spaces
            ing = Recipe.ingredients[i].split(' ', 3)
            if len(ing) > 1:
                # If first or second elts are fractions, tries to evaluate to a float
                ing[0] = fracToFloat(ing[0])
                ing[1] = fracToFloat(ing[1])
                # If first or second elts are fractions, adds them.
                try:
                    ing[0] = float(ing[0]) + float(ing[1])
                    del ing[1]
                except ValueError:
                    ing[0] = float(ing[0])
                Recipe.ingredients[i] = ing

    def convert(self):
        book = openpyxl.load_workbook('conversions.xlsx', data_only = True)

        sheetCols =  {
        # 'teaspoons' : 'U',
        # 'tablespoons' : 'V',
        # 'oz' : 'X',
        'cups' : 'Y',
        }

        def normalize(item):
            # Handles the cases where case matters
            if item == 'T':
                return 'tablespoons'
            if item == 't':
                return 'teaspoons'
            # Converts item to lowercase and tries to find it in spreadsheet
            item = item.lower()
            book.active = 1
            sheet = book.active
            for row in sheet.iter_rows():
                for cell in row:
                    if item == cell.value:
                        item = row[0].value
            return item

        def volToGram(amount, unit, ingredient):
            if unit not in sheetCols.keys():
                return -1

            # Normalizes passed information and opens sheet
            unit = normalize(unit)
            ingredient = normalize(ingredient)
            book.active = 0
            sheet = book.active

            # Iterates thru sheet looking for given ingredient
            for cell in sheet['P']:
                if ingredient == cell.value:
                    ratio = sheet[sheetCols[unit]][cell.row - 1].value
                    return int(round(amount * ratio))

            return -1

        for i, ing in enumerate(Recipe.ingredients):
            if len(ing) >= 3:
                grams = volToGram(ing[0], ing[1], ing[2])
                if grams > 0: 
                    Recipe.ingredients[i][0] = grams