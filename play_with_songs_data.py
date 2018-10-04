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
    songs1['text_lines'] = songs1['text'].str.split('\n')

    songs1['first_byte_lines'] = songs1['text_lines'].apply(lambda txt_lines: txt_lines[:[len(t.strip()) for t in txt_lines].index(0)])
    songs1['first_byte'] = songs1['first_byte_lines'].apply(lambda l: "\n".join(l))

    songs1['byte_with_suf'] = songs1['song'] + '\n' \
                              + songs1['artist'] + '\n----------------\n' \
                              + songs1['first_byte']+'\nthis is the end of the byte\n\n'

    fh = open('bytes_%d.txt' %(n), 'w')
    fh.writelines(songs1['byte_with_suf'].astype('str').values)
    fh.close()




if __name__ == '__main__':
    songs = pd.read_csv('songdata.csv')
    write_to_file(songs, n=20, is_random=True)

    print count_words(songs, n=1000)
    print get_pairs_hist(songs, n=2000)

    # yuval file:
    d = pd.read_excel('/home/igor/Downloads/1001dataset.xlsm')
    lyrs = pd.read_excel('/home/igor/Downloads/1001dataset.xlsm',sheet_name='lyrics')
    lyr_cols = [col for col in lyrs.columns if col.startswith('LYRICS')]

    i_min=51
    i_max=100
    fh = open('heb_from_csv_s%d_e%d.txt' %(i_min, i_max), 'w')
    for i, lyr in lyrs.iterrows():
        if i<i_min or i>i_max:
            continue
        try:
            fh.write(u'\n'.join(lyr[lyr_cols].dropna().values).encode('utf8').strip())
            fh.write('\n%d ------------------------- %d\n' %(i, i))
        except:
            print 'bassa', i

    fh.close()