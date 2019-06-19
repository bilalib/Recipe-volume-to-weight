from Recipe import *
import os

link = "https://www.allrecipes.com/recipe/8265/funnel-cakes-iv/?internalSource=hub%20recipe&referringContentType=Search"
# r = Recipe.from_link(link)
r = Recipe.from_string("3 eggs")
r.multiply(3)
r.convert_recipe()
print(r.prettify())