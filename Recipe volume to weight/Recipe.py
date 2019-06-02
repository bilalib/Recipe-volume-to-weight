import requests
from lxml import html
import openpyxl
import io
from fractions import Fraction

class Recipe(object):

    def __init__(self, ingredients):
        Recipe.ingredients = ingredients
        Recipe.parseIngList(self)
        Recipe.selection = list()

    @classmethod
    def fromLink(self, link):
        return self(Recipe.ingsFromLink(self, link))

    # Scrapes the Allrecipes link, getting the list of ingredients
    def ingsFromLink(self, link):
        with requests.get(link) as page:    
            tree = html.fromstring(page.content)
        return tree.xpath('//*[@id="lst_ingredients_1"]/li/label/span/text()')

    def parseIngList(self):

        def fracToFloat(frac):
            if '/' in frac:
                frac = list(map(float, frac.split('/')))
                return frac[0] / frac[1]
            else:
                return frac
        
        for i, ing in enumerate(Recipe.ingredients):
            # Splits ing such that number is seperate from unit and name
            splitAmount = 1
            for char in ing:
                if char.isalpha():
                    break
                if char == ' ':
                    splitAmount += 1
            ing = ing.split(' ', splitAmount)

            if len(ing) > 1:
                # If first or second elts are fractions, 
                # tries to evaluate to a float
                ing[0] = fracToFloat(ing[0])
                ing[1] = fracToFloat(ing[1])
                # Converts mixed numbers (e.x. 1 1/4) to one float (e.x. 1.25)
                try:
                    ing[0] = float(ing[0]) + float(ing[1])
                    del ing[1]
                except ValueError:
                    ing[0] = float(ing[0])

            Recipe.ingredients[i] = ing

    def volToGrams(self):
        book = openpyxl.load_workbook('conversions.xlsx', data_only = True)

        # Maps ingredient names to its column of the spreadsheet
        sheetCols =  {
        # 'teaspoons' : 'U',
        # 'tablespoons' : 'V',
        # 'oz' : 'X',
        'cups' : 'Y',
        }

        def normalize(item):
            # Handles situations where case matters
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

        def convert(amount, unit, ingredient):
            # Normalizes passed information and opens sheet
            unit = normalize(unit)
            ingredient = normalize(ingredient)
            book.active = 0
            sheet = book.active

            # Checks if the unit of measurement is known
            if unit not in sheetCols.keys():
                return -1

            # Iterates through sheet looking for given ingredient
            for cell in sheet['P']:
                if ingredient == cell.value:
                    # Converts the ingredient if it is found
                    ratio = sheet[sheetCols[unit]][cell.row - 1].value
                    return int(amount * ratio)
            return -1

        # Tries to convert each ingredient in ingredients
        for i, ing in enumerate(Recipe.ingredients):
            if len(ing) >= 3 and Recipe.inSelection(self, ing[2]):
                grams = convert(ing[0], ing[1], ing[2])
                if grams > 0: 
                    Recipe.ingredients[i][0] = grams
                    Recipe.ingredients[i][1] = 'grams'

    # Outputs the ingredient list in a readable format
    def prettify(self):
        # Creates stringIO to write each ingredient.
        # Goes through the amount of each ingredient first.
        with io.StringIO() as buffer:   
            for i, ing in enumerate(Recipe.ingredients):
                amount = ing[0]
                amountToBuffer = str(amount)
                # Converts amounts between 0 and 1 to fractions
                if amount < 1 and ing[1] != 'grams':
                    frac = str(Fraction(amount).limit_denominator())
                    if len(frac) <= 4:
                        amountToBuffer = frac
                # Converts floats representing ints 
                # (e.x. 1.0, 3.0) to int (e.x. 1, 3)
                elif type(amount) == float:
                    if amount.is_integer():
                        amountToBuffer = str(int(amount))

                # Writes the ingredient unit and name
                buffer.write(amountToBuffer + ' ' + ' '.join(
                    map(str, ing[1:])) + '\n')
            return buffer.getvalue()
    
    # Use to determine if user wants to convert the ingredient
    def inSelection(self, ing):
        if not Recipe.selection:
            return True
        if ing in Recipe.selection:
            return True
        return False