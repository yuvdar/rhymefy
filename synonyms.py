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

        cWord = Word(word)
        # syns = cWord.synonyms('all')

        syns = []
        word_data = cWord.data
        # if pos is not None:
        #     word_data = [l for l in word_data if l['partOfSpeech'] == pos]
        for rel_word_list in word_data:
            syns.extend([s.word for s in rel_word_list['syn']])

        if syns:
            all_syns.extend(syns)
    all_syns.extend(word_list)
    return list(set(all_syns))


def find_rhymes(word1, word2, depth1=2, depth2=2):
    words1 = syns(word1)
    if depth1==2:
        words1 = syns(words1)

    words2 = syns(word2)
    if depth2==2:
        words2 = syns(words2)

    l1 = [last_syllables(w) for w in words1]
    l2 = [last_syllables(w) for w in words2]

    w1 = pd.DataFrame({'word': words1, 'syl': l1})
    w1 = w1[w1.syl != False]

    w2 = pd.DataFrame({'word': words2, 'syl': l2})
    w2 = w2[w2.syl != False]

    return w1, w2, pd.merge(w1, w2, on='syl')

WORD1,WORD2 = 'peach', 'elbow'
WORD1,WORD2 = 'midnight', 'blow'
WORD1,WORD2 = 'me', 'lights'
WORD1,WORD2 = 'self', 'lights'
WORD1,WORD2 = 'chair', 'her'
WORD1,WORD2 = 'say', 'withdraw'
WORD1,WORD2 = 'sea', 'self'
WORD1,WORD2 = 'heat', 'go'
WORD1,WORD2 = 'door', 'stairway'
WORD1,WORD2 = 'couches', 'drink'
WORD1,WORD2 = 'seat', 'drink'
WORD1,WORD2 = 'table', 'pouring'
WORD1,WORD2 = 'wine', 'smile'
WORD1,WORD2 = 'look', 'easy'
WORD1,WORD2 = 'time', 'serious'
WORD1,WORD2 = 'text', 'you'

w1, w2, m = find_rhymes(WORD1,WORD2)
w1, w2, m = find_rhymes(WORD1,WORD2, depth1=1)
w1, w2, m = find_rhymes(WORD1,WORD2, depth1=1, depth2=2)
w1, w2, m = find_rhymes(WORD1,WORD2, depth1=1, depth2=1)

joint_syl = list(set(w1.syl.unique()).intersection(set(w2.syl.unique())))
fh = open('rhyme_%s_%s.txt'%(WORD1,WORD2), 'w')
for syl in joint_syl:
    fh.write('\n')
    fh.write(syl + ':\n\t')
    fh.write(", ".join(w1[w1.syl == syl].word.values))
    fh.write('\n\t')
    fh.write(", ".join(w2[w2.syl == syl].word.values))
fh.close()

for syl in joint_syl:
    print syl, ':'
    print w1[w1.syl == syl].word.values
    print w2[w2.syl == syl].word.values

def print_tripplet(g):
    print g.name
    print '\t'+g['word_x'].unique()
    print '\t'+g['word_y'].unique()