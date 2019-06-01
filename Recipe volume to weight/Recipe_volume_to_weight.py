from Menus import *
from Recipe import *






link = 'https://www.allrecipes.com/recipe/16822/cake-mix-cinnamon-rolls/?internalSource=previously%20viewed&referringContentType=Homepage'
recipe = Recipe.fromLink(link)
print(recipe.ingredients, '\n\n')
recipe.convert()
print(recipe.ingredients)
