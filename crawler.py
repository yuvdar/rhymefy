import scrapy
import requests
from lxml import etree
from lxml import html


WEB = 'https://www.rhymezone.com/r/rhyme.cgi?Word={}&typeofrhyme=perfect'


def get_ryhme(word):
    page = requests.get(WEB.format(word))
    tree = html.fromstring(page.content)
    found = False
    lst_s = []
    for e in tree.iter():
        if e.text == '2 syllables':
            found = False
        if found:
            if e.text:
                lst_s.append(e.text.replace('-',''))
        if e.text == '1 syllable':
            found = True

    return lst_s

print get_ryhme('girl')