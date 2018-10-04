import requests
import pandas as pd
from BeautifulSoup import BeautifulSoup


def extract_lyrics(uri):
    r = requests.get(uri)
    soup = BeautifulSoup(r.content)
    lyrics = soup.find('div', {'class': "item-lyrics-content"})
    return clean_lyrics(lyrics.getText(separator='\n'))


def clean_lyrics(lyrics):
    lyr_lst = lyrics.split('\n')[-7:-1]
    return '\n'.join(lyr_lst)


def extract_artist(uri):
    r = requests.get(uri)
    soup = BeautifulSoup(r.content)
    songs = soup.findAll('div', {'class': 'category-item artists-items'})
    artist_lst = []
    for song in songs:
        artist_lst.append((song.a.text, song.a['href']))
    return artist_lst


def extract_all():
    r = requests.get('https://xmusic.co.il/artists')
    soup = BeautifulSoup(r.content)
    artists = soup.findAll('div', {'class': 'category-item'})
    lyrics = []
    for artist in artists:
        link_art = artist.a['href'].replace('artists', 'lyrics')
        lyrics.extend([(artist.a['title'], link_lyr[0], extract_lyrics(link_lyr[1])) for link_lyr in extract_artist(
            link_art)])
    a = pd.DataFrame(lyrics)
    fh = open('bytes.txt', 'w')
    for i, r in a.iterrows():
        fh.write(r[2].encode('utf8') + '\n %d ----------- %d \n' %(i,i))
    fh.close()



def main():
    art_lyr = []
    for link_lyr in extract_artist('https://xmusic.co.il/lyrics/%D7%A2%D7%95%D7%9E%D7%A8-%D7%90%D7%93%D7%9D'):
        print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
        print 'extract song  : ' + link_lyr[0]
        print 'extract from  : ' + link_lyr[1]
        lyr_s =extract_lyrics(link_lyr[1])
        art_lyr.append(lyr_s)

extract_all()
