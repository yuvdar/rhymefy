import pandas as pd
from nltk.tokenize import RegexpTokenizer
import numpy as np
import gensim


def standardize_text(df, text_field):
    df[text_field] = df[text_field].str.replace(r"http\S+", "")
    df[text_field] = df[text_field].str.replace(r"http", "")
    df[text_field] = df[text_field].str.replace(r"@\S+", "")
    df[text_field] = df[text_field].str.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
    df[text_field] = df[text_field].str.replace(r"@", "at")
    df[text_field] = df[text_field].str.lower()
    return df


def get_translated(file_name):
    lines = open(file_name).readlines()
    lines = [l for l in lines if len(l)>2]

    # Gather songs
    songs = []
    current_song = []
    for l in lines:
        if l.find('------') == -1:
            current_song.append(l)
        else:
            songs.append(current_song)
            current_song = []

    # Take only the last k lines
    k = 6
    songs = [song for song in songs if len(song) >= k]

    agg_lines = []
    for i in range(k):
        line = [song[-1-i] for song in songs]
        agg_lines.append(line)

    data = pd.DataFrame({i: agg_lines[i] for i in range(k)})
    data['translated'] = True
    return data


def expand_data(data, word2vec, number_of_lines=6):
    tokenizer = RegexpTokenizer(r'\w+')
    for i in range(number_of_lines):
        standardize_text(data, i)
        data['t' + str(i)] = data[i].apply(tokenizer.tokenize)
        data['v' + str(i)] = data['t' + str(i)].apply(lambda x: get_average_word2vec(x, word2vec))
    return data

def filter_song(song):
    for i in range(len(song)):
        if song[i].find('this is the end of the song') != -1:
            return song[:i]
    return []


def get_original(file_name):
    lines = open(file_name).readlines()
    lines = [l for l in lines if len(l.strip())>2]

    # Gather songs
    songs = []
    current_song = []
    for l in lines:
        if l.find('------') == -1:
            current_song.append(l)
        else:
            songs.append(current_song)
            current_song = []

    # Take only the last k lines
    k = 6
    songs = [filter_song(song) for song in songs]
    songs = [song for song in songs if len(song) >= k]

    agg_lines = []
    for i in range(k):
        line = [song[-1-i] for song in songs]
        agg_lines.append(line)

    data = pd.DataFrame({i: agg_lines[i] for i in range(k)})
    data['translated'] = False
    return data


def get_average_word2vec(tokens_list, vector, generate_missing=False, k=300):
    if len(tokens_list)<1:
        return np.zeros(k)
    if generate_missing:
        vectorized = [vector[word] if word in vector else np.random.rand(k) for word in tokens_list]
    else:
        vectorized = [vector[word] if word in vector else np.zeros(k) for word in tokens_list]
    length = len(vectorized)
    summed = np.sum(vectorized, axis=0)
    averaged = np.divide(summed, length)
    return averaged


def main():
    k = 6
    data = get_translated('heb_from_csv_s0_e50_en.txt', k=k)
    data2 = get_original('songs_700.txt', k=k)
    all_data = data.append(data2, ignore_index=True)
    all_data.to_hdf('songs_sample.h5', 'sample')
    tokenizer = RegexpTokenizer(r'\w+')

    # Run once:
    word2vec_path = "models/GoogleNews-vectors-negative300.bin"
    word2vec = gensim.models.KeyedVectors.load_word2vec_format(word2vec_path, binary=True)
    for i in range(k):
        standardize_text(all_data, i)
        all_data['t' + str(i)] = all_data[i].apply(tokenizer.tokenize)
        all_data['v' + str(i)] = all_data['t' + str(i)].apply(lambda x: get_average_word2vec(x, word2vec))

    cnn_data = []
    labels = all_data['translated']
    for _, row in all_data.iterrows():
        row_data = np.vstack([row['v%d'%i] for i in range(k)])
        cnn_data.append(row_data)



if __name__=='__main__':
    main()