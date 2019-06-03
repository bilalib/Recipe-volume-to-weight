import requests
from lxml import html
import openpyxl
import io


class Recipe(object):
    def __init__(self, ingredients):
        self.ingredients_old = list(ingredients)
        self.ingredients = list(ingredients)
        self.parse_ing_list()
        self.selection = list()

    @classmethod
    def from_link(cls, link):
        path = "//span[@class='recipe-ingred_txt added']/text()"
        # Scrapes the Allrecipes link, getting the list of ingredients
        def ings_from_link(link):
            with requests.get(link) as page:
                tree = html.fromstring(page.content)
            return tree.xpath(path)

        return cls(ings_from_link(link))

    @classmethod
    def from_string(cls, recipeString):
        recipeList = recipeString.split("\n")
        return cls(recipeList)

    def parse_ing_list(self):

        def frac_to_float(frac):
            if "/" in frac:
                frac = [float(x) for x in frac.split("/")]
                return frac[0] / frac[1]
            else:
                return frac

        for i, ing in enumerate(self.ingredients): 
            if len(ing) > 1:
                # Splits ingredient so that amount, unit, and name are seperated
                split_amount = 1
                for char in ing:
                    if char.isalpha():
                        break
                    if char == " ":
                        split_amount += 1
                ing = ing.split(" ", split_amount)

            # If first or second elts are fractions, converts them to float
            ing[0] = frac_to_float(ing[0])
            ing[1] = frac_to_float(ing[1])
            # Converts mixed numbers (e.x. 1 1/4) to one float (e.x. 1.25)
            try:
                ing[0] = float(ing[0]) + float(ing[1])
                del ing[1]
            except ValueError:
                ing[0] = float(ing[0])

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
                    self.ingredients[i][0] = grams
                    self.ingredients[i][1] = "grams"

    # Outputs the ingredient list in a readable format
    def prettify(self):
        # Creates stringIO to write each ingredient. 
        # Goes through the amount of each ingredient first.
        with io.StringIO() as buffer:
            for i, ing in enumerate(self.ingredients):
                if ing[1] == "grams":
                    buffer.write(" ".join([str(elt) for elt in ing]))
                else:
                    buffer.write(self.ingredients_old[i])
                buffer.write("\n")
            return buffer.getvalue()