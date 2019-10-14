# Recipe-volume-to-weight
Scrapes popular recipe websites; converts measurements to grams; multiplies ingredients.

## Supported websites
* jocooks
* justonecookbook
* allrecipes
* marthastewart
* smittenkitchen
* budgetbytes
* damndelicious

## Basic usage

### Starting from a ```string``` or ```list```
Although the main usage is to get a recipe from one of the above websites using a link, a recipe can also be parsed (into ingrident, unit, and amount) from a string or ```list```.
An instance of recipe can be (equivalently) initialized with the follwing code.

```r = Recipe.from_string("3 cups flour\n1 tbsp sugar\n1 egg", "string")```

```r = Recipe.from_list(["3 cups flour", "1 tbsp sugar", "1 egg"], "list")```

The next section will describe how to use a recipe once it is initialized.

### Starting from a url
Consider this url to AllRecipes, which is a ```Recipe``` for "Pumpkin Waffles with Apple Cider Syrup". 
```
link = "https://www.allrecipes.com/recipe/65691/pumpkin-waffles-with-apple-cider-syrup/?internalSource=editorial_2&referringId=78&referringContentType=Recipe%20Hub"
```
Then issuing the following code will scrape the link and create an instance of ```Recipe``` with the parsed ingredient ```list```.
```
r = Recipe.from_link(link)
r.convert_recipe()
```
Now, ```r.ings``` is a ```list``` of ```dictionary```, one corresponding to each ingredient, ordered in the same way the ingredients were in the original recipe. 

Each ```dictionary``` contains the following keys.

key | value
------------- | -------------
```name```| The name of the ingredient
```unit```| The unit of measure for the ingredient
```selected```| True if the ingredient was selected to be converted, False otherwise.
```changed```| True if ingredient was converted, False otherwise.
```amount```| The amount of the ingredient. This will be converted to grams if ```changed == True```.

The first ingredient in the recipe on the website is  2 1/2 cups all-purpose flour. Hence, ```r.ings[0]``` contains the dictionary correspoding to flour.
```
print(r.ings[0]["amount"], r.ings[0]["unit"], r.ings[0]["name"])
```
outputs the following.
```
302 grams flour
```
```r.multiply(self, multiplier)``` will multiply all ingredients that it can (even those not selected for conversion) by the multiplier. The multiplier can be a decimal as well, to scale the recipe up or down. Furthermore, ```r.prettify()``` will return a ```string``` with the formatted, converted recipe, ready to print.

Using this process to get the converted ```list``` of ingredients ```r.ings``` is useful when one wants to use ```Recipe``` to interface with other code. If this is not the case, there is a function to scrape, convert, print, and multiply, all in one line.

### Automatically scrape, convert, print, multiply
The static method ```convert_print(source, source_type, multiplier=1)``` will do all of the above automatically, printing the entire recipe to standard output.

Example:

```Recipe.convert_print("3 cups flour\n1 tbsp sugar\n1 egg", "string", 2)``` and

```Recipe.convert_print(["3 cups flour", "1 tbsp sugar", "1 egg"], "list", 2)``` both print

```
724 grams flour
26 grams sugar
2 egg
```
A link in the form of a ```string``` may also be used.

## Scraper
The scraper is its own class, and can be used standalone. The supported websites are given at the top of this page. Suppose that ```link``` is a ```string``` containing a url to a supported website. To just get a ```list``` of ingredients, one may use the static method ```auto_scrape_ings```. ```Scraper.auto_scrape_ings(link)``` will return a ```list``` of ingredients, in the order corresponding to the original recipe. ```Scraper``` can also scrape the title, ingredients, and directions from a link. The following code will also automatically detect the website of a given link.
```s = Scraper.auto_scrape(link)```
will create the instance and scrape the wesbite. Then, ```s.ings``` will is a ```list``` of the ingredients, ```s.dirs``` is a ```list``` of the directions, and ```s.title``` is a ```string``` the name of the recipe.
