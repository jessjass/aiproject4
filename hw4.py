import csv
import math
ingreds = [] # all ingredients
training = {} # training recipes by class/cuisine -> dictionary of lists of lists
ingreds_class = {} # unique ingredients by class -> dictionary of sets
cuisine_probs = {} # probabilities of cuisines -> dictionary of probablities
ingred_cusine_probs = {} # probablities of ingredients by class -> dictionary of dictionaries
ingred_probs = {} # probablities of ingredients out of all ingredients -> dictionary

l = 1
k = 1000

def read_training(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            if row[1] in training:
                training[row[1]].append(row[2:])
                cuisine_probs[row[1]] = (cuisine_probs[row[1]]*1794 + 1)/1794
            else:
                training[row[1]] = [row[2:]]
                cuisine_probs[row[1]] = 1/1794


def read_ingredients(filename):
    with open(filename) as file:
        for line in file:
            ingreds.append(line.rstrip())


def make_sets_of_ingreds():
    for key in training:
        for recipe in training[key]:
            if key in ingreds_class:
                ingreds_class[key].update(recipe)
            else:
                ingreds_class[key] = set(recipe)


def calc_ingred_prob_by_cuisine():
    for cuisine in training:
        ingred_cusine_probs[cuisine] = {}
        for recipe in training[cuisine]:
            for ingred in recipe:
                if ingred in ingred_cusine_probs[cuisine]:
                    ingred_cusine_probs[cuisine][ingred] = ((ingred_cusine_probs[cuisine][ingred] * len(ingreds_class[cuisine])) + 1) / len(ingreds_class[cuisine])
                else:
                    ingred_cusine_probs[cuisine][ingred] = 1 / len(ingreds_class[cuisine])


def calc_ingred_probs():
    for cuisine in training:
        for recipe in training[cuisine]:
            for ingred in recipe:
                if ingred in ingred_probs:
                    ingred_probs[ingred] = (ingred_probs[ingred]*2398 + 1)/2398
                else:
                    ingred_probs[ingred] = 1/2398



def classifiy_recipe(recipe):
    max = 0
    max_cuisine = None
    temp_cuisine = None
    for c in ingreds_class:
        sum = 0
        temp = 0
        for ingred in recipe:
            p = 0
            for cuisine in ingreds_class:
                if ingred in cuisine:
                    p = (ingred_cusine_probs[cuisine][ingred]*len(ingreds_class[cuisine]) + l)/(len(ingreds_class[cuisine] + l*k))
                else:
                    p = l/(len(ingreds_class[cuisine]) + l*k)
                temp_cuisine = cuisine
            sum += math.log10(p)
        temp = math.log10(cuisine_probs[cuisine]) + sum
        if temp > max:
            max = temp
            max_cuisine = temp_cuisine
    return max_cuisine




read_ingredients('ingredients.txt')
read_training('training.csv')
make_sets_of_ingreds()
calc_ingred_prob_by_cuisine()
calc_ingred_probs()
print(training)
print(ingreds_class)
print(cuisine_probs)
print(ingred_cusine_probs)
print(len(ingreds))
print(ingred_probs)
print(classifiy_recipe(["dry white wine","leaf parsley","greek yogurt","mussels","shallots","olive oil"]))