from Recipe import *
import os

link = "https://www.allrecipes.com/recipe/71003/coconut-cream-pound-cake/?internalSource=streams&referringId=276&referringContentType=Recipe%20Hub&clickId=st_recipes_mades"

r = Recipe.from_string("some really salty salt to salt with\n2 cups flour\n3 dishes of good stuff and stuff\n4")
r.convert_recipe()
r.multiply(4)
print(r.prettify())