from Menus import *
from Recipe import *

recipe = Recipe()
link = 'https://www.allrecipes.com/recipe/23431/to-die-for-fettuccine-alfredo/?internalSource=previously%20viewed&referringContentType=Homepage'
ingredients = recipe.getIngList(link)
ingredients = recipe.parseIngList(ingredients)
print(ingredients)