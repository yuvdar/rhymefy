from vocabulary.vocabulary import Vocabulary as vb
import pandas as pd
import re


def last_syllables(word):
    pron = vb.pronunciation(re.sub('[^A-Za-z0-9]+', '', word), format='dict')
    if pron is False:
        return False
    else:
        d = pd.DataFrame(pron.values())
        if 'arpabet' in d['rawType'].values:
            pr = d[d['rawType'] == 'arpabet'].iloc[0]['raw']
            return ''.join(pr.split(' ')[-2:])
        else:
            return False


def syns(word_list):
    if type(word_list) == str:
        word_list = [word_list]
    all_syns = []
    for word in word_list:
        syns = vb.synonym(re.sub('[^A-Za-z0-9]+', '', word), format='dict')
        if syns:
            all_syns.extend(syns.values())
    all_syns.extend(word_list)
    return list(set(all_syns))


def find_rhymes(word1, word2):
    words1 = syns(syns(word1))
    words2 = syns(syns(word2))

    l1 = [last_syllables(w) for w in words1]
    l2 = [last_syllables(w) for w in words2]

    w1 = pd.DataFrame({'word': words1, 'syl': l1})
    w1 = w1[w1.syl != False]

    w2 = pd.DataFrame({'word': words2, 'syl': l2})
    w2 = w2[w2.syl != False]

    pd.merge(w1, w2, on='syl')


find_rhymes('pretty', 'woman')