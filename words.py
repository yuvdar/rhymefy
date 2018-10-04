import gensim
from crawler import get_rhyme
from synonyms import syns
"""
download google model and put it under ./models
https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing
"""
MODEL = gensim.models.KeyedVectors.load_word2vec_format('./models/GoogleNews-vectors-negative300.bin', binary=True)


def get_similar(word, n=10):
    MODEL.most_similar(positive=[word], topn=n)


def rhyme_zone(word1, word2):
    return MODEL.most_similar_to_given(word1,[w for w in get_rhyme(word2) if w in MODEL])


def rhyme_zone_sort(word1, word2):
    un_sort = [(word, MODEL.similarity(word1, word)) for word in get_rhyme(word2) if word in MODEL]
    return list(reversed(sorted(un_sort,key=lambda x: x[1])))


def rhyme_zone_sort_syn(word1, word2):
    un_sort = [(word, MODEL.similarity(word1, word)) for word in get_rhyme(word2) if word in MODEL]
    un_sort = [(w[0], word2) for w in un_sort if w[1] > 0.35]
    #print un_sort
    for word in syns(word2):
        #print word
        temp = [(w, MODEL.similarity(word1, w)) for w in get_rhyme(word) if w in MODEL]
        un_sort.extend([(w[0], word) for w in temp if w[1] > 0.35])
    return un_sort

#rhyme_zone_sort_syn('girl', 'pretty')