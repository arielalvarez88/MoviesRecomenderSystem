

""" Folder data\raw\recipes_reviews has files with the recipe_id as the name of the file.
Inside each files are the reviews for that particular recipe. That is the data I got from the BigOven.com. """


import ConfigParser

configParser = ConfigParser.ConfigParser()
configParser.read("./config.txt")

k_neighbors = configParser.get("config", 'k_neighbors')

print(k_neighbors)
