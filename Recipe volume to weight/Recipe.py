import openpyxl
import io
from Scraper import *
from fractions import Fraction

class Recipe(object):
    def __init__(self, ings):
        self.ings = list(ings)
        self.parse_ing_list()
        self.ings_old = tuple(ings)
        self.ings_changed = [False] * len(self.ings)
        self.selected = [False] * len(self.ings)

    # Scrapes the link, getting the list of ings
    @classmethod
    def from_link(cls, link):
        return cls(Scraper(link).ings)

    @classmethod
    def from_string(cls, recipe_string):
        recipe_list = recipe_string.split("\n")
        return cls(recipe_list)

    @staticmethod
    def convert_print(source, source_type):
        if source_type == "link":
            recipe = Recipe.from_link(source)
        elif source_type == "string":
            recipe = Recipe.from_string(source)
        elif source_type == "list":
            recipe = Recipe(source)

        recipe.convert_recipe()
        print(recipe.prettify())

    def parse_ing_list(self):
        def frac_to_float(frac):
            if "/" in frac[:4]:
                frac = tuple(float(x) for x in frac.split("/"))
                frac = frac[0] / frac[1]
            return frac

        for i, ing in enumerate(self.ings):
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
            # Fixes situations like this: [1, .25, ...] --> [1.25, ...]
            try:
                ing[0] = float(ing[0]) + float(ing[1])
                del ing[1]
            except ValueError:
                if type(ing[0]) == str and ing[0].isdigit():
                    ing[0] = float(ing[0])
            self.ings[i] = ing

        self.ings = tuple(self.ings)

    def convert_recipe(self):

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
                
        # Returns -1 if ing couldn't be converted
        def convert_ing(ing_idx):
            ing = self.ings[ing_idx]

            if len(ing) < 3 or not in_selection(ing_idx):
               return -1

            # Normalizes and names given information
            amount = float(ing[0])
            unit = normalize(ing[1])
            ing_name = normalize(ing[2])

            # Checks if the unit of measurement is known. 
            # Maps ingredient names to its column of the spreadsheet
            sheet_cols = {
                # 'oz' : 'X', 'teaspoons' : 'U', 'tablespoons' : 'V', "lb.": "AD", 
                "cups": "Y"
            }

            # Opens spreadsheet of conversions
            book.active = 0
            sheet = book.active

            if unit in sheet_cols.keys():
                # Iterates through sheet looking for given ingredient
                for cell in sheet["P"]: 
                    if ing_name == cell.value:
                        # Converts the ingredient if it is found
                        ratio = sheet[sheet_cols[unit]][cell.row - 1].value
                        return amount * ratio
            return -1

        # Use to determine if user wants to convert the ingredient
        def in_selection(ing_idx):
            return all(not x for x in self.selected) or self.selected[ing_idx]

        # Tries to convert each ingredient in ings
        for i, ing in enumerate(self.ings):
            grams = convert_ing(i)
            if grams > 0:
                ing[0] = grams
                ing[1] = "grams"
                self.ings_changed[i] = True

    # Outputs the ingredient list in a readable format
    def prettify(self):
        # Creates stringIO to write each ingredient. 
        # Goes through the amount of each ingredient first.
        with io.StringIO() as buffer:
            for i, ing in enumerate(self.ings):
                if self.ings_changed[i]:
                    # Makes floats less ugly by converting to int or rounding
                    if type(ing[0]) == float:
                        if ing[0].is_integer():
                            ing[0] = int(ing[0])
                        else:
                            ing[0] = round(ing[0], 1)
                    buffer.write(" ".join([str(x) for x in ing]))
                else:
                    buffer.write(self.ings_old[i])
                buffer.write("\n")
            return buffer.getvalue()

    def multiply(self, multiplier):
        for _, ing in enumerate(self.ings):
            if type(ing[0]) == int or type(ing[0]) == float:
                ing[0] *= multiplier
        self.ings_changed = [True] * len(self.ings)

    def select(self, *args):
        self.selected = [False] * len(self.ings)
        for _, ing_idx in enumerate(args):
            self.selected[ing_idx - 1] = True