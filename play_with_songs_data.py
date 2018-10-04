import pandas as pd

def get_pairs(entry):
    lines = entry['text'].split('\n')
    lines = [l.strip() for l in lines if len(l.strip()) > 0]
    sufs = [l.split()[-1] for l in lines]
    s1 = pd.Series(sufs[:-1])
    s2 = pd.Series(sufs[1:])

    pairs = pd.concat([s1, s2], axis=1)
    pairs = pairs[pairs.index % 2 == 0]
    pairs_reverse = pd.concat([s2, s1], axis=1)
    pairs_reverse = pairs_reverse[pairs_reverse.index % 2 == 0]
    pairs = pd.concat([pairs, pairs_reverse], axis=0).drop_duplicates()
    pairs = pairs[pairs[0]<pairs[1]]

    return pairs[0] + ' ' + pairs[1]

def get_pairs_hist(songs, n=1000):
    songs1 = songs.head(n)
    pairs = []
    for k, song in songs1.iterrows():
        if k%100 == 0:
            print k
        pairs.append(get_pairs(song))
    all_pairs = pd.concat(pairs).reset_index(drop=True)
    print all_pairs.value_counts()


def count_words(songs, n=1000):
    all_songs_in_one_line = " ".join(songs.head(n)['text'].astype('str').values)
    num_words = len(all_songs_in_one_line.split(" "))
    return num_words


def write_to_file(songs, n=10, is_random=False):
    if is_random:
        songs1 = songs.sample(n).copy()
    else:
        songs1 = songs.head(n).copy()
    songs1['text_with_suf'] = songs1['song'] + '\n' \
                              + songs1['artist'] + '\n----------------\n' \
                              + songs1['text']+'\nthis is the end of the song\n\n'
    fh = open('try_song_%d.txt' %(n), 'w')
    fh.writelines(songs1['text_with_suf'].astype('str').values)
    fh.close()




if __name__ == '__main__':
    songs = pd.read_csv('songdata.csv')
    write_to_file(songs, n=20, is_random=True)

    print count_words(songs, n=1000)
    print get_pairs_hist(songs, n=2000)

    # yuval file:
    d = pd.read_excel('/home/igor/Downloads/1001dataset.xlsm')