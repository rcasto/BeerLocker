import os
import json
import util

data_directory = './data/'
beer_data_files = []
beer_bag = {}

# get the names of all beer data files
for filename in os.listdir(data_directory):
    # filter out any non-json files
    if filename.endswith('.json'):
        beer_data_files.append(filename)

# Go through file names list, open each file, analyze it, repeat
for filename in beer_data_files:
    with open(data_directory + filename, 'r') as file:
        try:
            beer_data = json.load(file)

            for beer in beer_data:
                tokens = util.wordTokenizer(beer['description'])
                tokens = util.normalizeWords(tokens)
                tokens = util.removePunctuation(tokens)
                tokens = util.removeStopWords(tokens, 'english')

                util.createOrUpdateWordBag(tokens, beer_bag)
        except:
            print '%s is invalid JSON' % filename

# Print out the top 50 words
util.print_top_n(beer_bag, 50)