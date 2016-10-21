import json
import requests

baseApi = 'http://api.brewerydb.com/v2'
beersApi = baseApi + '/beers'
stylesMenuApi = baseApi + '/menu/styles'

beersFile = open('english_ipa.json', 'a')
beerStyle = 2

def prettyPrint(jsonObj):
    return json.dumps(jsonObj, indent=4, sort_keys=True)

def getBeerStyles(key):
    return requests.get(stylesMenuApi, params= {
        'key': key
    }).json()

def getNumBeerPagesForStyle(key, styleId):
    return requests.get(beersApi, params = { 
        'key': key,
        'styleId': styleId,
        'p': 1
    }).json()['numberOfPages']

def getBeersForPage(key, styleId, page):
    return requests.get(beersApi, params = { 
        'key': key,
        'styleId': styleId,
        'p': page
    }).json()['data']

def getPropOrDefault(obj, prop, default = ''):
    if prop in obj:
        return obj[prop]
    else:
        return default

def filterBeerInfo(beers):
    filteredBeers = []
    for beer in beers:
        # Record only verified beers
        if 'status' in beer and beer['status'] == 'verified':
            filteredBeers.append({
                'abv': getPropOrDefault(beer, 'abv'),
                'name': getPropOrDefault(beer, 'name'),
                'ibu': getPropOrDefault(beer, 'ibu'),
                'style': beer['style']['name'] if (('style' in beer) and ('name' in beer['style'])) else '',
                'styleId': getPropOrDefault(beer, 'styleId'),
                'id': getPropOrDefault(beer, 'id'),
                'description': getPropOrDefault(beer, 'description'),
                'createDate': getPropOrDefault(beer, 'createDate')
            })
    return filteredBeers

try:
    config = open('config.json', 'r')
except (OSError, IOError):
    print 'config file cannot be opened or found'
else:
    try:
        configJson = json.load(config)
    except ValueError:
        print 'File is invalid JSON'
    else:
        api_key = configJson['api_key']
        numPages = getNumBeerPagesForStyle(api_key, beerStyle)
        beerLocker = []

        print 'Total beer pages: %d' % numPages

        for i in range(1, numPages + 1):
            print 'Fetching beers from page: %d' % i

            beers = getBeersForPage(api_key, beerStyle, i)
            beerLocker.extend(filterBeerInfo(beers))
        
        beersFile.write(prettyPrint(beerLocker))

    config.close()

beersFile.close()