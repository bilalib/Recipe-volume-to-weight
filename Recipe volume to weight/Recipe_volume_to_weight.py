from Recipe import *
import os

link = "https://www.allrecipes.com/recipe/236165/fluffy-and-delicious-pancakes/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%206"
recipe = Recipe.from_link(link)
recipe.vol_to_grams()
print(recipe.prettify())