from Recipe import *
import os


link = "https://www.budgetbytes.com/strawberry-shortcake/"

r = Recipe.from_link(link)
r.select(3)
r.convert_recipe()
print(r.prettify())