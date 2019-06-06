from Recipe import *
import os

link = "https://www.allrecipes.com/recipe/8265/funnel-cakes-iv/?internalSource=hub%20recipe&referringContentType=Search"

r = Recipe.from_string(recipe_str)
r.convert_recipe()
print(r.prettify())
r.multiply(1/2)
print(r.prettify())