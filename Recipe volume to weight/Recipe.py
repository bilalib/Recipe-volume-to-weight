import openpyxl
import io
from Scraper import Scraper
from fractions import Fraction


class Recipe(object):

    def __init__(self, ings):
        self.book = openpyxl.load_workbook("conversions.xlsx", data_only=True)
        self.ings_original = tuple(ings)
        self.ings = tuple({"changed": False, "selected": True} for ing in ings)
        self.parse_ing_list()

    # Scrapes the link, getting the list of ings
    @classmethod
    def from_link(cls, link):
        return cls(Scraper.auto_scrape(link))

    @classmethod
    def from_string(cls, recipe_string):
        recipe_list = recipe_string.split("\n")
        return cls(recipe_list)

    @staticmethod
    def convert_print(source, source_type, multiplier=1):
        if source_type == "link":
            recipe = Recipe.from_link(source)
        elif source_type == "string":
            recipe = Recipe.from_string(source)
        elif source_type == "list":
            recipe = Recipe(source)
        
        if multiplier != 1:
            recipe.multiply(multiplier)
        recipe.convert_recipe()
        print(recipe.prettify())

    def parse_ing_list(self):
        def frac_to_float(frac):
            if "/" in frac[:4]:
                frac = tuple(float(x) for x in frac.split("/"))
                frac = frac[0] / frac[1]
            return frac

        def normalize(item):
            # T and t conflict, so we deal with them before 
            # converting everything to lowercase
            case_matters = {"T": "tablespoons", "t": "teaspoons"}
            if item in case_matters.keys():
                return case_matters[item]
            # Converts item to lowercase and tries to find it in spreadsheet
            item = item.lower()
            self.book.active = 1
            sheet = self.book.active
            for row in sheet.iter_rows(values_only=True):
                if any(item == cell for cell in row):
                    return row[0]
            return item

        for i, ing in enumerate(self.ings_original):
            # Splits ingredient so that amount, unit, and name are seperated
            split_amount = 1
            for char in ing:
                if not (char.isdigit() or char in " ./-"):
                    break
                if char in " -":
                    split_amount += 1
            ing = ing.split(" ", split_amount)
            if len(ing) < 3:
                self.ings[i]["selected"] = False
                continue

            # If first or second elts are fractions, converts them to float
            ing[:2] = [frac_to_float(x) for x in ing[:2]]
            # Fixes situations like this: [1, .25, ...] --> [1.25, ...]
            whole, frac = ing[:2]
            try:
                ing[0] = float(whole) + float(frac)
                del ing[1]
            except ValueError:
                if type(whole) == str and whole.isdigit():
                    ing[0] = float(whole)
            
            self.ings[i].update({"amount": float(ing[0]), "unit": 
                                 normalize(ing[1]), "name": normalize(ing[2])})

    def convert_recipe(self):

        # Opens spreadsheet of conversions
        self.book.active = 0
        sheet = self.book.active
        known_ings = sheet["P"]
        # Maps ingredient unit to its column of the spreadsheet
        sheet_cols = {
            # 'oz' : 'X', 'teaspoons' : 'U', 'tablespoons' : 'V', "lb.": "AD", 
            "cups": "Y"
        }

        # Tries to convert each ingredient in ings
        for _, ing in enumerate(self.ings):
            if not (ing["selected"] and ing["unit"] in sheet_cols.keys()):
               continue
            # Iterates through sheet looking for given ingredient
            for cell in (cell for cell in 
                         known_ings if ing["name"] == cell.value): 
                # Converts the ingredient if it is found
                ing_row = sheet_cols[ing["unit"]]
                ratio = sheet[ing_row][cell.row - 1].value
                ing["amount"] = round(ing["amount"] * ratio)
                ing["unit"] = "grams"
                ing["changed"] = True

    # Outputs the ingredient list in a readable format
    def prettify(self, numbered=False):

        # Makes floats less ugly by converting to int or rounding
        def clean_float(number):
            if type(number) != float:
                return str(number)
            if number.is_integer():
                return str(int(number))

            whole = int(number)
            decimal = number - whole
            frac = str(Fraction(decimal).limit_denominator())
            if len(frac) <= 4:
                # 0 1/3 --> 1/3
                return str(whole) + " " + frac if whole > 0 else frac

            return round(number, 1)

        # Creates stringIO to write each ingredient. 
        # Goes through the amount of each ingredient first.
        with io.StringIO() as buffer:
            for i, ing in enumerate(self.ings):
                if numbered:
                    buffer.write(str(i + 1) + ") ")
                if self.ings[i]["changed"]:
                    fragments = tuple(ing.values())[3:]
                    buffer.write(clean_float(ing["amount"]) + " " 
                                 + " ".join([str(x) for x in fragments]))
                else:
                    buffer.write(self.ings_original[i])
                buffer.write("\n")
            return buffer.getvalue()
        
    def multiply(self, multiplier):
        for _, ing in enumerate(ing for ing in 
                                self.ings if "amount" in ing.keys()):
            ing["amount"] *= multiplier
            ing["changed"] = True

    def select(self, *args):
        self.selected = [False] * len(self.ings)
        for _, ing_idx in enumerate(args):
            self.ings[ing_idx - 1]["selected"] = True