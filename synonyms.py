from vocabulary.vocabulary import Vocabulary as vb
import json
import pandas as pd

d = json.decoder.JSONDecoder()


def last_syllables(word):
    pron = vb.pronunciation(word)
    if pron is False:
        return None
    else:
        return ''.join(d.decode(pron)[-1]['raw'].split(' ')[-2:])


def rhymes(w1, w2):
    l1 = last_syllables(w1)
    l2 = last_syllables(w2)
    if l1 is not None and l2 is not None and l1 == l2:
        return True
    else:
        return False


def syns(word_list):
    if type(word_list) == str:
        word_list = [word_list]
    all_syns = []
    for word in word_list:
        all_syns.extend([a['text'].encode('utf-8').strip() for a in d.decode(vb.synonym(word))])
    return list(set(all_syns))
words1 = syns(syns('chance'))
words2 = syns(syns('hand'))

l1 = [last_syllables(w) for w in words1]
l2 = [last_syllables(w) for w in words2]

w1 = pd.DataFrame({'word': words1, 'syl': l1})
w1 = w1[w1.syl != False]

w2 = pd.DataFrame({'word': words2, 'syl': l2})
w2 = w2[w2.syl != False]

pd.merge(w1, w2, on='syl')

