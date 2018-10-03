import gensim
"""
download google model and put it under ./models
https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing
"""
MODEL = gensim.models.KeyedVectors.load_word2vec_format('./models/GoogleNews-vectors-negative300.bin', binary=True)


def get_similar(word, n=10):
    MODEL.most_similar(positive=[word], topn=n)