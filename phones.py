import numpy as np
import pronouncing as pr

PHONES = ['AA','AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G', 'HH', 'IH',
          'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH', 'UW',
          'V', 'W', 'Y', 'Z', 'ZH']


def last_phone(word):
    phones = pr.phones_for_word(word)
    if phones:
        last = phones[0].split(' ')[-1]
        return np.array([(last.find(x)!=-1) for x in PHONES]).astype(int)
    else:
        return np.zeros(len(PHONES))
