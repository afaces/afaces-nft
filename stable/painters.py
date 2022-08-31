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

owner = "pharmapsychotic"
project = "clip-interrogator"
branch = "main"

artists, flavors, mediums, movements = formatGithubList(owner, project, "data/artists.txt", branch),\
                                       formatGithubList(owner, project, "data/flavors.txt", branch),\
                                       formatGithubList(owner, project, "data/mediums.txt", branch),\
                                       formatGithubList(owner, project, "data/movements.txt", branch)

'''for britishFamousPainting in britishFamousPaintings:
    for spanishPainter in spanishPainters:
        print(britishFamousPainting[:-2] + " by " + spanishPainter)'''

