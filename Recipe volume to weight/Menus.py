from Ingredient_measurements import *
from tkinter import *
from tkinter import messagebox

class Menus(object):
    """Makes GUI and provides functionality to buttons"""

    def __init__(self):
        Menus.conversions = Ingredient_measurements()
        Menus.win = Tk()
        Menus.win.geometry('300x300')
        # mainMenu buttons
        Menus.conversionsB = Button(Menus.win, 
                                    text = 'Open unit conversion dictionary',
                                    command = lambda: Menus.conversionsMenu(self))
        Menus.convertB = Button(Menus.win, text = 'Convert a recipe')
        Menus.allrecipesB = Button(Menus.win, text = 'Enter Allrecipes URL')

        # conversionsMenu buttons
        Menus.addB = Button(Menus.win, text = 'Add ingredient', 
                            command = lambda: Menus.conversions.addIngredient())
        Menus.removeB = Button(Menus.win, text = 'Remove ingredient', 
                               command = lambda: Menus.conversions.removeIngredient())
        Menus.ingredientB = Button(Menus.win, text= 'Edit an ingredient', 
                                   command = lambda: Menus.ingredientMenu(self))
        Menus.backB = Button(Menus.win, text = 'Go back', 
                             command = lambda : Menus.mainMenu(self))
        Menus.saveB = Button(Menus.win, text = 'Save and re-print', 
                             command = lambda: Menus.conversions.save())

        # ingredientMenu buttons
        Menus.ing = None
        Menus.addIngB = Button(Menus.win, text = 'Add or replace a unit',
                               command = lambda: Menus.conversions.addReplaceUnit(Menus.ing))
        Menus.removeUnitB = Button(Menus.win, text = 'Remove a unit', 
                                   command = lambda: Menus.conversions.removeUnit(Menus.ing))
        Menus.backIngB = Button(Menus.win, text = 'Go back', 
                                command = lambda: Menus.conversionsMenu(self))
        
    def clear(self):
        for widgets in Menus.win.winfo_children():
            widgets.forget()

    def mainMenu(self):
        Menus.clear(self)
        Menus.conversionsB.pack()
        Menus.convertB.pack()
        Menus.allrecipesB.pack()
        Menus.win.mainloop()
    
    def conversionsMenu(self):
        Menus.clear(self)
        Menus.conversions.print()
        Menus.backB.pack()
        Menus.addB.pack() 
        Menus.removeB.pack()
        Menus.ingredientB.pack()
        Menus.win.mainloop()

    def ingredientMenu(self):
        Menus.clear(self)
        Menus.ing = input('Ingredient name: ')
        Menus.conversions.printIng(Menus.ing)
        # Buttons
        Menus.backIngB.pack()
        Menus.addIngB.pack()
        Menus.removeUnitB.pack()
        Menus.win.mainloop()