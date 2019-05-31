import pickle
DICTIONARY_FILE_NAME = 'ingredient_measurements_pickle.txt'

class Ingredient_measurements(object):
    """This class provides functionality for the dictionary of ingredient 
    measurements. It pickles the dictionary in ingredient_measurements_dict."""

    # Loads up the dictionary as conversions
    with open(DICTIONARY_FILE_NAME, 'rb') as conversionsFile:
        try:
            conversions = pickle.load(conversionsFile)
        except EOFError:
            conversions = {}

    def save(self):
        # Uses pickle to store dictionary as a file.
        with open(DICTIONARY_FILE_NAME, 'wb+') as \
            Ingredient_measurements.conversionsFile:
            pickle.dump(Ingredient_measurements.conversions, 
                        Ingredient_measurements.conversionsFile)
        print('Saved.')
        Ingredient_measurements.print(self)

    # The name of the ingredient to add should be a string, passed as ingredient.
    def addIngredient(self):
        try:
            ingName = Ingredient_measurements.normalize(self, input('Ingredient to add: ').lower())
            if ingName in Ingredient_measurements.conversions.keys():
                print('Already in dictionary.')
            elif ingName == '':
                print('Invalid input.')
            else:
                Ingredient_measurements.conversions[ingName] = {}
                print('Added.')
                Ingredient_measurements.save(self)
        except:
            print('Invalid input.')

    def removeIngredient(self):
        ingName = Ingredient_measurements.normalize(self, input(
            'Ingredient to remove: '))
        try:
            del Ingredient_measurements.conversions[ingName]
            print('Deleted.')
            Ingredient_measurements.save(self)
        except:
            print('Invalid input.')

    def saveIng(self, ing):
        # Uses pickle to store dictionary as a file.
        with open(DICTIONARY_FILE_NAME, 'wb+') as \
            Ingredient_measurements.conversionsFile:
            pickle.dump(Ingredient_measurements.conversions, 
                        Ingredient_measurements.conversionsFile)
        print('Saved.')
        Ingredient_measurements.printIng(self, ing)
    
    # Prints a specific ingredient given its name
    def printIng(self, ingKey):
        ingKey = Ingredient_measurements.normalize(self, ingKey)
        try:
            print(ingKey)
            for unitKey in sorted(Ingredient_measurements.conversions[ingKey].keys()):
                print('{:3}{:11}{:1}{:3}'.format(
                    ' ', unitKey, ': ', int(round(
                        Ingredient_measurements.conversions[ingKey][unitKey]))))
        except:
            print(ingKey, 'is an invalid input. Please go back.')

    # Prints the entire dictionary
    def print(self):
        print('Unit conversion dictionary;')
        print('Volumetric measurement on left, grams on right.\n')
        for key in Ingredient_measurements.conversions.keys():
            Ingredient_measurements.printIng(self, key)
        print('\n')

    def normalize(self, input):
        input = input.lower()
        # Changes common measurements to dictionary-standard forms
        equivalencies = {
            'tablespoon': ['tbsp', 'tablespoons'],
            'teaspoon': ['tsp', 'teaspoons'],
            'cup': ['cups'],
            'white sugar' : ['sugar'],
            'powdered sugar': ['confectioner\'s sugar', 'confectioner sugar', 'confectioners sugar'],
            'flour': ['all-purpose flour'],
            'brown sugar': ['dark brown sugar', 'light brown sugar']
            }
        for key in equivalencies.keys():
            if input in equivalencies[key]:
                input = key
        return input

    # Appends the dictionary with a new unit, or replaces an existing one
    def addReplaceUnit(self, ingName):
        ingName = Ingredient_measurements.normalize(self, ingName)
        unitKey = Ingredient_measurements.normalize(self, input('Name of unit: '))
        print('Grams of', ingName, 'per', unitKey, end = ': ')
        unitValue = float(input())
        Ingredient_measurements.conversions[ingName][unitKey] = unitValue
        print('Added and saved.')
        Ingredient_measurements.autofill(self, ingName, unitKey, unitValue)
        Ingredient_measurements.saveIng(self, ingName)
    
    # Fills in cups, tablespoons, teaspoons given one of them.
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

    # Deletes a unit from the dictionary
    def removeUnit(self, ingredient):
        del Ingredient_measurements.conversions[ingredient][
            Ingredient_measurements.normalize(self, input('Name of unit: '))]
        print('Removed and saved.')
        Ingredient_measurements.saveIng(self, ingredient)