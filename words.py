import gensim
from crawler import get_rhyme
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
    return list(reversed(sorted([(word, MODEL.similarity(word1, word)) for word in get_rhyme(word2) if word in MODEL],key=lambda
        x: x[1])))

