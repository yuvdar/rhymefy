import requests
from lxml import html


WEB_RHYME = 'https://www.rhymezone.com/r/rhyme.cgi?Word={}&typeofrhyme=perfect'


def get_rhyme(word):
    page = requests.get(WEB_RHYME.format(word))
    tree = html.fromstring(page.content)
    found = False
    lst_s = []
    for e in tree.iter():
        if e.text:
            if 'syllable' in e.text and found:
                found = False
            if found:
                if not e.text.replace('\n', ''):
                    break
                lst_s.append(e.text.replace('-', ''))
            if 'syllable' in e.text and not found:
                found = True

    return lst_s

print get_rhyme('Working')
