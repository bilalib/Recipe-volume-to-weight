from Recipe import *
import os

link = "https://www.allrecipes.com/recipe/12682/apple-pie-by-grandma-ople/?recipeType=Recipe&servings=8&isMetric=false"
recipe = Recipe.from_link(link)
recipe.vol_to_grams()
print(recipe.prettify())