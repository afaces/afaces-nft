import requests
from bs4 import BeautifulSoup


def scrapeSiteText(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output


def getRawText(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    return soup.find_all(text=True)


def getGitHubRawTextURL(owner, name, path, branch):
    return "https://raw.githubusercontent.com/" + owner + "/" + name + "/" + branch + "/" + path


def formatList(text):
    output = ''
    for t in text:
        output += '{} '.format(t)
    return output.split('\n')


def formatGithubList(owner, name, path, branch):
    return formatList(getRawText(getGitHubRawTextURL(owner, name, path, branch)))

'''
lines = str(scrapeSiteText("https://en.wikipedia.org/wiki/List_of_Spanish_painters").split('\n')).split('Contents:')[1][200:20050].split('\n')
lines = lines[0].split(" ', ' ")[:-1]

spanishPainters = []
for i in lines:
    if "[ edit ]" in i:
        continue
    spanishPainters.append(i)

lines3 = str(scrapeSiteText("https://en.wikipedia.org/wiki/100_Great_Paintings").split('\n')).split('Contents:')[0]
lines3 = lines3.split(" ', '")[62:268]

britishFamousPaintings = []
for i in lines3:
    text = i.split(":")
    for i in range(len(text)):
        if i % 2:
            britishFamousPaintings.append(text[i].split("(")[0])
'''

owner = "pharmapsychotic"
project = "clip-interrogator"
branch = "main"

artists, flavors, mediums, movements = formatGithubList(owner, project, "data/artists.txt", branch)[:-1],\
                                       formatGithubList(owner, project, "data/flavors.txt", branch)[:-1],\
                                       formatGithubList(owner, project, "data/mediums.txt", branch)[:-1],\
                                       formatGithubList(owner, project, "data/movements.txt", branch)[:-1]

'''for britishFamousPainting in britishFamousPaintings:
    for spanishPainter in spanishPainters:
        print(britishFamousPainting[:-2] + " by " + spanishPainter)
'''


# print(artists)
# print(mediums)
# print(flavors)
# print(movements)

def buildStableDiffusionPrompt():
    return "test"
    
adjectives = ["intricate"]

# CHARACTERS
faces = ["wide", "plump", "afflicted", "square", "distrustful", "sucked", "sweet", "hard", "punished", "trusting", "hardened", "sad", "expressive", "fine", "fresh", "thin", "round", "wild", "dry", "nice", "calm", "inexpressive", "jovial", "long"]
front = ["wide", "wrinkled", "low", "narrow", "smooth", "convex"]
eyes = ["absent", "low", "bluish", "concentrated", "awake", "impenetrable", "expressionless", "intense", "malicious", "very black", "serene", "dreamy", "tender", "sad", "alive"]
nose = ["aquiline", "flat", "wide", "round", "fine", "long", "pointed", "straight", "crooked"]
mouth = ["fine", "fresh", "large", "hard", "small", "round", "kissy", "talkative"]
neck = ["short", "thin", "thick", "elegant", "long"]
teeth = ["aligned", "white", "yellowish"]
cheeks = ["plump", "flat", "puffy", "round", "rough", "smooth", "soft", "red"]
lips = ["narrow", "thin", "large", "hermetic", "thin", "sensual"]
eyelashes = ["thick", "long", "black", "clear", "curly"]
eyebrows = ["arched", "thick", "together", "thin", "separated"]
ears = ["big", "long", "round", "small"]
color = ["pale", "pink", "albino", "brown", "ash", "yellowish", "whitish", "oily", "tan", "olive", "dark"]
hair = ["abandoned", "shiny", "dirty", "brown", "curly", "cared", "fine", "silky", "oily", "smooth", "black", "wavy", "blond", "messy", "rough", "kinky"]
hands = ["agile", "white", "warm", "rough", "delicate", "fine", "clumsy", "large", "thick", "rough", "young", "sensitive"]
legs = ["thin", "thick", "puny", "skinny", "strong", "dry", "chubby", "robust"]
general_appearance = ["tall", "athletic", "short", "robust", "corpulent", "slight", "slender", "skinny", "nervous", "weak", "firm", "strong", "fat", "agile", "sporty", "young", "mature", "skinny", "thin", "old", "healthy", "solid", "hard-working"]
dress = ["simple", "sophisticated", "discreet", "elegant", "poor", "abandoned"]
physic = ["effeminate", "agile", "albino", "tall", "mannered", "old man", "ancient", "nasty", "attractive", "bass", "beardless", "pot-belly", "squinting", "bald", "brown", "short", "chepped", "blind", "classic", "lame", "corpulent", "thin", "careless", "ungainly", "elegant", "sickly", "dwarf", "curved", "sickly", "slender", "skinny", "spiked", "skeletal", "ugly", "thin", "nasal", "jaunty", "giant", "fat", "fatty", "great", "handsome", "hirsute", "childish", "hunchback", "young man", "youth", "slow", "light", "cleansed", "solid", "ripe", "one-armed", "modern", "brown", "mute", "muscular", "big noses", "obese", "haggard", "tidy", "pale", "bow-legged", "bully", "redhead", "furry", "little", "quick", "chubby", "plump", "blond", "healthy", "sophisticated", "dirty", "stutterer", "clumsy", "one-eyed", "manly", "fast", "old", "nice", "short-leg", "long-legged"]

# ENVIRONMENTS

landscapes = ["abandoned", "cozy", "nice", "isolated", "width", "ancient", "peaceful", "arid", "nice", "bustling", "warm", "chaotic", "abundant", "contaminated", "cosmopolitan", "coastal", "clear", "deserted", "high", "charming", "enormous", "steep", "close", "evocative", "famous", "fascinating", "fertile", "ugly", "cold", "leafy", "great", "smelly", "historical", "industrial", "bright", "flat", "rainy", "modern", "mountainous", "Dark", "dangerous", "little", "picturesque", "placid", "populated", "remote", "noisy", "rural", "dry", "sure", "serene", "silent", "sunny", "gloomy", "dirty", "calm", "traveled", "tourist", "urban"]
sky = ["blue", "gray", "gunmetal", "red", "black", "starry", "cloudy", "clear", "sunny", "rainy", "clear", "covered"]
sea = ["blue", "greenish", "rough", "serene", "riotous", "choppy", "undulating", "clear", "calm"]
houses = ["low", "tall", "old", "modern", "humble", "big", "small", "stately", "single-family", "flats", "old", "blocks", "shops", "with garden", "with pool"]
mountains = ["high", "low", "green", "bare", "rounded", "dry", "pointed"]
forest = ["green", "thick", "leafy", "dark", "autumnal", "snowy", "humid", "solitary", "refreshing"]
trees = ["tall", "short", "thick", "thin", "corpulent", "leafy", "rounded", "elongated", "dry"]
cities = ["bustling", "quiet", "calm", "noisy", "pleasant", "unpleasant", "funny", "boring", "modern", "old", "historical"]
fields = ["green", "yellow", "dark", "dry", "arid", "fertile", "cultivated"]

# INTERIORS

interiors = ["clean", "distinguished", "dry", "detailed", "professional", "magical", "transformative", "exciting", "visionary", "wild", "urban", "natural", "rugged", "ethereal", "earthy", "organic", "revolutionary", "dynamic", "professional", "modern", "historic", "bold", "colorful", "fascinating", "creative", "complete", "mysterious", "strong", "detailed", "focus", "fierce", "loud", "unconventional", "iconic", "raw", "tranquil", "radiant", "pleasant", "natural", "graceful", "delightful", "delicate", "timely", "free flowing", "effective", "impactful", "progressive", "naturalistic", "spontaneous", "monumental", "innovative", "soaring", "illuminating", "enlightening", "status", "international", "passionate", "leading", "earthly", "energetic", "enthusiastic", "whole", "dark", "vast", "deep", "far", "mountainous", "dim", "entire", "continental", "western", "domestic", "white", "cool", "black", "african", "northern", "hollow", "southern", "solar", "spacious", "remote", "hot", "dry", "red", "arid", "rich", "hydrophobic", "unknown", "gloomy", "warm", "beautiful", "darkened", "empty", "cavernous", "soft", "stellar", "shadowy", "like", "gothic", "eastern", "bright", "decorated", "smooth", "liquid", "lighted", "elegant", "rural", "brazilian", "rugged", "luxurious", "heated", "nuclear", "brown", "distant", "baroque", "north", "chinese", "typical", "lunar", "dutch", "magnificent", "cold", "brachial", "wild", "dorsal", "vaulted", "century", "bare", "east", "mysterious", "mexican", "ornate", "clean", "grey", "forested", "hilly", "gray", "south", "plain", "light", "alternate", "lit", "impressive"]

if __name__ == '__main__':
    stablediffusion = "stablediffusion \""
    print(stablediffusion + buildStableDiffusionPrompt() + "\"")