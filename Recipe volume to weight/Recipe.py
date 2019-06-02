import requests
from lxml import html
import openpyxl
import io
from fractions import Fraction

class Recipe(object):

    def __init__(self, ingredients):
        self.ingredients = ingredients
        self.parseIngList()
        self.selection = list()

    @classmethod
    def fromLink(cls, link):

        # Scrapes the Allrecipes link, getting the list of ingredients
        def ingsFromLink(link):
            with requests.get(link) as page:    
                tree = html.fromstring(page.content)
            return tree.xpath('//*[@id="lst_ingredients_1"]/li/label/span/text()')

        return cls(ingsFromLink(link))

    @classmethod
    def fromString(cls, recipeString):
        recipeList = recipeString.split('\n')
        return cls(recipeList)

    def parseIngList(self):

        def fracToFloat(frac):
            if '/' in frac:
                frac = list(map(float, frac.split('/')))
                return frac[0] / frac[1]
            else:
                return frac
        
        for i, ing in enumerate(self.ingredients):
            # If the ingredient is just one word like 'salt', nothing to parse.
            if len(ing) <= 1:
                continue

            # Splits ingredient so that amount, unit, and name are seperated
            splitAmount = 1
            for char in ing:
                if char.isalpha():
                    break
                if char == ' ':
                    splitAmount += 1
            ing = ing.split(' ', splitAmount)

            # If first or second elts are fractions, converts them to float
            ing[0] = fracToFloat(ing[0])
            ing[1] = fracToFloat(ing[1])
            # Converts mixed numbers (e.x. 1 1/4) to one float (e.x. 1.25)
            try:
                ing[0] = float(ing[0]) + float(ing[1])
                del ing[1]
            except ValueError:
                ing[0] = float(ing[0])

            self.ingredients[i] = ing

    def volToGrams(self):
        book = openpyxl.load_workbook('conversions.xlsx', data_only = True)

        # Maps ingredient names to its column of the spreadsheet
        sheetCols =  {
        # 'teaspoons' : 'U', 'tablespoons' : 'V', 'oz' : 'X',
        'cups' : 'Y'
        }

        def normalize(item):
            # Handles the conflict where letter case matters
            if item == 'T':
                return 'tablespoons'
            if item == 't':
                return 'teaspoons'
            # Converts item to lowercase and tries to find it in spreadsheet
            item = item.lower()
            book.active = 1
            sheet = book.active
            for row in sheet.iter_rows(values_only = True):
                for cell in row:
                    if item == cell:
                        item = row[0]
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
        for i, ing in enumerate(self.ingredients):
            if len(ing) >= 3 and self.inSelection(ing[2]):
                grams = convert(ing[0], ing[1], ing[2])
                if grams > 0: 
                    self.ingredients[i][0] = grams
                    self.ingredients[i][1] = 'grams'

    # Outputs the ingredient list in a readable format
    def prettify(self):
        # Creates stringIO to write each ingredient.
        # Goes through the amount of each ingredient first.
        with io.StringIO() as buffer:   
            for i, ing in enumerate(self.ingredients):
                amount = ing[0]
                amountToBuffer = str(amount)
                # Converts amounts between 0 and 1 to fractions. Ex. .25 -> 1/4
                if amount < 1 and ing[1] != 'grams':
                    frac = str(Fraction(amount).limit_denominator())
                    if len(frac) <= 4:
                        amountToBuffer = frac
                # Converts floats representing ints to ints. Ex. 3.0 -> 3
                elif type(amount) == float:
                    if amount.is_integer():
                        amountToBuffer = str(int(amount))

                # Writes the ingredient unit and name
                buffer.write(amountToBuffer + ' ' + ' '.join(
                    map(str, ing[1:])) + '\n')
            return buffer.getvalue()
    
    # Use to determine if user wants to convert the ingredient
    def inSelection(self, ing):
        if not self.selection:
            return True
        if ing in self.selection:
            return True
        return False