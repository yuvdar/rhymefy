import requests
from BeautifulSoup import BeautifulSoup


def extract_lyrics(uri):
    r = requests.get(uri)
    soup = BeautifulSoup(r.content)
    lyrics = soup.find('div', {'class': "item-lyrics-content"})
    return lyrics.p.getText(separator='\n')


def main():
    uri = 'https://xmusic.co.il/lyrics/%D7%90%D7%A4%D7%95%D7%A7%D7%9C%D7%99%D7%A4%D7%A1%D7%94/%D7%9C%D7%A9%D7%91%D7%95%D7%A8-%D7%90%D7%AA-%D7%94%D7%9B%D7%9C%D7%9C%D7%99%D7%9D'
    print extract_lyrics(uri)
