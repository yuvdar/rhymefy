from vocabulary.vocabulary import Vocabulary as vb
import pandas as pd
import re
from thesaurus import Word
import pronouncing as pr


def last_syllables(word):
    phones = pr.phones_for_word(word)
    if phones:
        return ''.join(phones[0].split(' ')[-2:])
    else:
        return False


def syns(word_list):
    if type(word_list) == str:
        word_list = [word_list]
    all_syns = []
    for word in word_list:
        syns = Word(word).synonyms()
        if syns:
            all_syns.extend(syns)
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

    return w1, w2, pd.merge(w1, w2, on='syl')


w1, w2, m = find_rhymes('peach', 'elbow')

joint_syl = list(set(w1.syl.unique()).intersection(set(w2.syl.unique())))
for syl in joint_syl:
    print syl, ':'
    print w1[w1.syl == syl].word.values
    print w2[w2.syl == syl].word.values

def print_tripplet(g):
    print g.name
    print '\t'+g['word_x'].unique()
    print '\t'+g['word_y'].unique()