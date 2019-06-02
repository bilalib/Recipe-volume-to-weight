from Recipe import *

link = 'https://www.allrecipes.com/recipe/236165/fluffy-and-delicious-pancakes/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%206'
recipe = Recipe.fromLink(link)
recipe.volToGrams()
print(recipe.prettify())
