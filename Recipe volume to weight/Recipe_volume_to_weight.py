from Recipe import *






link = 'https://www.allrecipes.com/recipe/16822/cake-mix-cinnamon-rolls/?internalSource=previously%20viewed&referringContentType=Homepage'
recipe = Recipe.fromLink(link)
recipe.volToGrams()
print(recipe.prettify())
