import nltk
"""
nltk.download('cmudict')
"""


def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)


def get_syllables(inp):
    entries = nltk.corpus.cmudict.entries()
    syllables = [syl for word, syl in entries if word == inp]
    return syllables


def doTheyRhyme(word1, word2, level=1):
  # first, we don't want to report 'glue' and 'unglue' as rhyming words
  # those kind of rhymes are LAME
  return word1 in rhyme(word2, level)
