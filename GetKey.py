from encrypt import vigenereEncryption
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from TextHandler import getAlphabet
from GetStatistics import getLetterStatistics

def fracCipher(cipher, keylen):
    list = []
    for i in range(keylen):
        list.append('') 
    i = 0
    for c in cipher:
        list[i % keylen] += c
        i += 1
    return list

def chi(dist, text, alphabet):
    sum = len(text)
    x = 0
    for i, letter in enumerate(alphabet):
        c = countletter(text, letter)
        e = dist[i]
        x += (c - e*sum)**2 / (e*sum)
    return x

def caeser(text, s, alphabet):
    cipher = ''
    for c in text:
        i = (alphabet.index(c) + s) % len(alphabet)
        cipher += alphabet[i]
    return cipher

def countletter(text, letter):
    count = 0
    for c in text:
        if c == letter:
            count += 1
    return count

def getKey(cipher, keylen):
    alphabet = getAlphabet()[0]
    dist = getLetterStatistics()

    cipherlist = fracCipher(cipher, keylen)
    key = ''
    for seq in cipherlist:
        min = np.inf
        for i in range(len(alphabet)):
            x = chi(dist, caeser(seq, i, alphabet), alphabet)
            if x < min:
                min = x
                c = alphabet[-i]
        key += c
    return key

def main():
    key = 'waddup'
    keylen = len(key)

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    dist = [0.0840581700543246, 0.01441026267065454, 0.018115831451301145, 0.05333526623125598, 0.1288683391320271,
            0.019733361818144824,
            0.02180868379824615, 0.08113593358969663, 0.05983590713951454, 0.0008799772121508067, 0.010386783047467903,
            0.0422363628964984,
            0.021355978758469146, 0.06785234694500397, 0.07513632016928116, 0.012444302020386986, 0.0007197501475106309,
            0.051176015788724084,
            0.056145598079309855, 0.09595566542554274, 0.02637642678386132, 0.0079121650491363, 0.03031852123135771,
            0.000699403853588069,
            0.018741479989419926, 0.0003611467171254756]

    # dist = [0.082,0.015,0.027,0.043,0.13,0.022,0.02,0.062,0.069,0.0015,0.0078,0.041,0.025,0.067,0.078,0.019,0.00096,0.059,0.062,0.096,0.027,0.0097,0.024,0.0015,0.02,0.00078]
    # ^distribution according to wiki

    with open('./Grimm stories/Ashputtel.txt', 'r') as f:
        text = f.read()
    text = ''.join([c for c in text if c.isalpha()])
    cipher = vigenereEncryption(text, key)

    print(getKey(cipher, keylen, dist, alphabet))

if __name__ == "__main__":
    main()

