import requests
from bs4 import BeautifulSoup

spain_url = "https://en.wikipedia.org/wiki/List_of_Spanish_painters"
res = requests.get(spain_url)
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

lines = str(output.split('\n')).split('Contents:')[1][200:20050].split('\n')
lines = lines[0].split(" ', ' ")[:-1]

spanishPainters = []
for i in lines:
    if "[ edit ]" in i:
        continue
    spanishPainters.append(i)

'''for painter in spanishPainters:
    print(painter)
'''

url = "https://en.wikipedia.org/wiki/100_Great_Paintings"
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

lines3 = str(output.split('\n')).split('Contents:')[0]
lines3 = lines3.split(" ', '")[62:268]

britishFamousPaintings = []
for i in lines3:
    text = i.split(":")
    for i in range(len(text)):
        if i % 2:
            britishFamousPaintings.append(text[i].split("(")[0])

for painting in britishFamousPaintings:
    print(painting)

print(len(britishFamousPaintings)) # 213 titles

print(len(spanishPainters))

for britishFamousPainting in britishFamousPaintings:
    for spanishPainter in spanishPainters:
        print(britishFamousPainting + ", by " + spanishPainter)