import pickle
DICTIONARY_FILE_NAME = 'ingredient_measurements_pickle.txt'

class Ingredient_measurements(object):
    """This class provides functionality for the dictionary of ingredient 
    measurements. It pickles the dictionary in ingredient_measurements_dict."""

    def __init__(self):
        # Loading is the dictionary that maps volumetric measurements to grams 
        # for every ingredient.
        with open(DICTIONARY_FILE_NAME, 'rb') as \
            Ingredient_measurements.conversionsFile:
            try:
                Ingredient_measurements.conversions = pickle.load(
                        Ingredient_measurements.conversionsFile)
            except EOFError:
                Ingredient_measurements.conversions = {}


    # The name of the ingredient to add should be a string, passed as ingredient.
    def addIngredient(self):
        ingredient = input('Ingredient name: ').lower()
        if ingredient in Ingredient_measurements.conversions.keys():
            print('Already in dictionary.')
        else:
            Ingredient_measurements.conversions[ingredient] = {}
            print('Added.')


    def removeIngredient(self):
        del Ingredient_measurements.conversions[
            input('Ingredient name: ').lower()]
        print('Deleted.')

    def save(self):
        # Uses pickle to store dictionary as a file.
        with open(DICTIONARY_FILE_NAME, 'wb+') as \
            Ingredient_measurements.conversionsFile:
            pickle.dump(Ingredient_measurements.conversions, 
                        Ingredient_measurements.conversionsFile)
        print('Saved.')
        Ingredient_measurements.print(self)

    def saveIng(self, ing):
        # Uses pickle to store dictionary as a file.
        with open(DICTIONARY_FILE_NAME, 'wb+') as \
            Ingredient_measurements.conversionsFile:
            pickle.dump(Ingredient_measurements.conversions, 
                        Ingredient_measurements.conversionsFile)
        print('Saved.')
        Ingredient_measurements.printIng(self, ing)
        
    def printIng(self, ingKey):
        print(ingKey)
        for unitKey in sorted(Ingredient_measurements.conversions[ingKey].keys()):
            print('{:3}{:11}{:1}{:3}'.format(
                ' ', unitKey, ': ', int(round(
                    Ingredient_measurements.conversions[ingKey][unitKey]))))

    def print(self):
        print('Unit conversion dictionary;')
        print('Volumetric measurement on left, grams on right.\n')
        for key in Ingredient_measurements.conversions.keys():
            Ingredient_measurements.printIng(self, key)
        print('\n')

    def normalize(self, input):
        input.lower()
        # Changes common measurements to dictionary-standard forms
        equivalencies = {
            'tablespoon': ['tbsp', 'tablespoons'],
            'teaspoon': ['tsp', 'teaspoons'],
            'cup': ['cups'],
            }
        for key in equivalencies.keys():
            if input in equivalencies[key]:
                input = key
        return input

    def addReplaceUnit(self, ingredient):
        unitKey = Ingredient_measurements.normalize(self, 
                                                    input('Name of unit: '))
        print('Grams of', ingredient, 'per', unitKey, end = ': ')
        unitValue = float(input())
        Ingredient_measurements.conversions[ingredient][unitKey] = unitValue
        print('Added and saved.')
        Ingredient_measurements.autofill(self, ingredient, unitKey, unitValue)
        Ingredient_measurements.saveIng(self, ingredient)

    def autofill(self, ingredient, unitKey, unitValue):
        autofilled = False
        if unitKey == 'cup':
            autofilled = True
            tbspValue = Ingredient_measurements.conversions[
                ingredient]['tablespoon'] = unitValue / 16
            print('working')
            Ingredient_measurements.conversions[ingredient][
                'teaspoon'] = tbspValue / 3
        if unitKey == 'tablespoon':
            autofilled = True
            Ingredient_measurements.conversions[ingredient][
                'cup'] = unitValue * 16
            Ingredient_measurements.conversions[ingredient][
                'teaspoon'] = unitValue / 3
        if unitKey == 'teaspoon':
            autofilled = True
            tbspValue = Ingredient_measurements.conversions[
                ingredient]['tablespoon'] = unitValue * 3
            Ingredient_measurements.conversions[ingredient][
                'cup'] = tbspValue * 16
        if autofilled: print('Autofilled other units.')

    def removeUnit(self, ingredient):
        del Ingredient_measurements.conversions[ingredient][
            Ingredient_measurements.normalize(self, normalize(input('Name of unit: ')))]
        print('Removed and saved.')
        Ingredient_measurements.saveIng(self, ingredient)