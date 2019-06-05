import openpyxl
import io
from Scraper import *

class Recipe(object):
    def __init__(self, ingredients):
        self.ingredients = list(ingredients)
        self.parse_ing_list()
        self.ingredients_old = tuple(ingredients)
        self.ingredients_changed = [False] * len(self.ingredients)
        self.selection = tuple()

    # Scrapes the link, getting the list of ingredients
    @classmethod
    def from_link(cls, link):
        return cls(Scraper(link).ings)

    @classmethod
    def from_string(cls, recipeString):
        recipeList = recipeString.split("\n")
        return cls(recipeList)

    def parse_ing_list(self):
        def frac_to_float(frac):
            if "/" in frac:
                frac = tuple(float(x) for x in frac.split("/"))
                frac = frac[0] / frac[1]
            return frac

        for i, ing in enumerate(self.ingredients):
            # Splits ingredient so that amount, unit, and name are seperated
            split_amount = 1
            for char in ing:
                if char.isalpha():
                    break
                if char == " ":
                    split_amount += 1
            ing = ing.split(" ", split_amount)
            # If first or second elts are fractions, converts them to float
            ing[:2] = [frac_to_float(x) for x in ing[:2]]
            # Converts mixed numbers (e.x. 1 1/4) to one float (e.x. 1.25)
            try:
                ing[0] = sum(float(x) for x in ing[:2])
                del ing[1]
            except ValueError:
                try:
                    ing[0] = float(ing[0])
                except:
                    pass

            self.ingredients[i] = ing

    def vol_to_grams(self):
        book = openpyxl.load_workbook("conversions.xlsx", data_only=True)

        def normalize(item):
            # T and t conflict, so we deal with them before 
            # converting everything to lowercase
            case_matters = {"T" : "tablespoons", "t": "teaspoons"}
            if item in case_matters.keys():
                return case_matters[item]
            # Converts item to lowercase and tries to find it in spreadsheet
            item = item.lower()
            book.active = 1
            sheet = book.active
            for row in sheet.iter_rows(values_only=True):
                for cell in (cell for cell in row if item == cell):
                    return row[0]
            return item
                

        def convert(ing):
            # Normalizes and names given information
            amount = ing[0]
            unit = normalize(ing[1])
            ingredient = normalize(ing[2])

            # Opens spreadsheet of conversions
            book.active = 0
            sheet = book.active

            # Checks if the unit of measurement is known. 
            # Maps ingredient names to its column of the spreadsheet
            sheet_cols = {
                # 'oz' : 'X', 'teaspoons' : 'U', 'tablespoons' : 'V', 
                "cups": "Y"
            }

            if unit in sheet_cols.keys():
                # Iterates through sheet looking for given ingredient
                for cell in sheet["P"]: 
                    if ingredient == cell.value:
                        # Converts the ingredient if it is found
                        ratio = sheet[sheet_cols[unit]][cell.row - 1].value
                        return int(amount * ratio)
            return -1

        # Use to determine if user wants to convert the ingredient
        def in_selection(ingName):
            if not self.selection:
                return True
            if ingName in self.selection:
                return True
            return False

        # Tries to convert each ingredient in ingredients
        for i, ing in enumerate(self.ingredients):
            if len(ing) >= 3 and in_selection(ing[2]):
                grams = convert(ing)
                if grams > 0:
                    ing[0] = grams
                    ing[1] = "grams"
                    self.ingredients_changed[i] = True

    # Outputs the ingredient list in a readable format
    def prettify(self):
        # Creates stringIO to write each ingredient. 
        # Goes through the amount of each ingredient first.
        with io.StringIO() as buffer:
            for i, ing in enumerate(self.ingredients):
                if self.ingredients_changed[i]:
                    # Makes floats less ugly by converting to int or rounding
                    if type(ing[0]) == float:
                        if ing[0].is_integer():
                            ing[0] = int(ing[0])
                        else:
                            ing[0] = round(ing[0], 1)
                    buffer.write(" ".join([str(x) for x in ing]))
                else:
                    buffer.write(self.ingredients_old[i])
                buffer.write("\n")
            return buffer.getvalue()

    def multiply(self, multiplier):
        for _, ing in enumerate(self.ingredients):
            ing[0] *= multiplier
        self.ingredients_changed = [True] * len(self.ingredients)