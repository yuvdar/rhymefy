import pandas as pd


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


def main():
    data = get_translated('heb_from_csv_s0_e50_en.txt')
    data2 = get_original('songs_700.txt')
    all_data = data.append(data2, ignore_index=True)
    all_data.to_hdf('songs_sample.h5', 'sample')

if __name__=='__main__':
    main()