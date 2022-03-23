import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
from TextHandler import getText, getAlphabet
from encrypt import vigenereEncryption, generateRandomKey
from GetStatistics import getLetterStatisticsInText

FONTSIZE = 12
mpl.rcParams.update({'font.family': 'serif', 'font.size': FONTSIZE})

def getDistributions(m, encrypted, key, s):
    path = './Grimm stories/*'
    files = glob.glob(path + "/*.txt")
    alphabet, A = getAlphabet()
    distribution_m = np.zeros(A**m)
    distribution_m1 = np.zeros(A ** (m - 1))
    if m < 2:
        return 0
    elif m > 2:
        distribution_m2 = np.zeros(A ** (m - 2))
    else:
        distribution_m2 = 1
    for file in files:
        text = getText(file)
        if encrypted:
            text = vigenereEncryption(text, key)
        if s > 1:
            text = text[0::s]
        for k in range(len(text)-m+1):
            subtext_m = text[k:k + m]
            i_m = 0
            for n in range(m):
                i_m += alphabet.index(subtext_m[n]) * A ** (m - n - 1)
            distribution_m[i_m] += 1

            subtext_m1_1 = text[k:k + m - 1]
            i_m1 = 0
            for n in range(m-1):
                i_m1 += alphabet.index(subtext_m1_1[n]) * A ** ((m - 1) - n - 1)
            distribution_m1[i_m1] += 1
            subtext_m1_2 = text[k + 1:k + m]
            i_m1 = 0
            for n in range(m-1):
                i_m1 += alphabet.index(subtext_m1_2[n]) * A ** ((m - 1) - n - 1)
            distribution_m1[i_m1] += 1

            if m > 2:
                subtext_m2_1 = text[k:k + m - 2]
                i_m2 = 0
                for n in range(m-2):
                    i_m2 += alphabet.index(subtext_m2_1[n]) * A ** ((m - 2) - n - 1)
                distribution_m2[i_m2] += 1
                subtext_m2_2 = text[k + 1:k + m - 1]
                i_m2 = 0
                for n in range(m-2):
                    i_m2 += alphabet.index(subtext_m2_2[n]) * A ** ((m - 2) - n - 1)
                distribution_m2[i_m2] += 1
                subtext_m2_3 = text[k + 2:k + m]
                i_m2 = 0
                for n in range(m-2):
                    i_m2 += alphabet.index(subtext_m2_3[n]) * A ** ((m - 2) - n - 1)
                distribution_m2[i_m2] += 1

    distribution_m = distribution_m / np.sum(distribution_m)
    distribution_m1 = distribution_m1 / np.sum(distribution_m1)
    if m > 2:
        distribution_m2 = distribution_m2 / np.sum(distribution_m2)
    return distribution_m, distribution_m1, distribution_m2


def getKm(m, encrypted=False, key='a', s=1):
    distribution_m, distribution_m1, distribution_m2 = getDistributions(m, encrypted, key, s)

    path = './Grimm stories/*'
    files = glob.glob(path + "/*.txt")
    alphabet, A = getAlphabet()

    k_m = 0
    for file in files:
        text = getText(file)
        if encrypted:
            text = vigenereEncryption(text, key)
        if s > 1:
            text = text[0::s]
        for k in range(len(text) - m + 1):
            subtext_m = text[k:k + m]
            i_m = 0
            for n in range(m):
                i_m += alphabet.index(subtext_m[n]) * A ** (m - n - 1)
            p_x1xm = distribution_m[i_m]
            if p_x1xm != 0:
                distribution_m[i_m] = 0

                subtext_m1_1 = text[k:k + m - 1]
                i_m1_1 = 0
                for n in range(m - 1):
                    i_m1_1 += alphabet.index(subtext_m1_1[n]) * A ** ((m - 1) - n - 1)
                p_x1xm1 = distribution_m1[i_m1_1]

                subtext_m1_2 = text[k + 1:k + m]
                i_m1_2 = 0
                for n in range(m - 1):
                    i_m1_2 += alphabet.index(subtext_m1_2[n]) * A ** ((m - 1) - n - 1)
                p_x2xm = distribution_m1[i_m1_2]

                if m > 2:
                    subtext_m2_2 = text[k + 1:k + m - 1]
                    i_m2 = 0
                    for n in range(m - 2):
                        i_m2 += alphabet.index(subtext_m2_2[n]) * A ** ((m - 2) - n - 1)
                    p_x2xm1 = distribution_m2[i_m2]
                else:
                    p_x2xm1 = 1

                k_m += p_x1xm * np.log2(p_x1xm * p_x2xm1 / (p_x1xm1 * p_x2xm))
    return k_m

def compareKm(maxKeyLength=45):
    nKeyWords = 100

    k_m_english = np.zeros(5)
    k_m_vigenere = np.zeros((5, nKeyWords))
    k_m_vigenere_mean = np.zeros(5)
    k_m_vigenere_std = np.zeros(5)

    keyLength = np.random.randint(2, maxKeyLength + 1, nKeyWords)
    keys = []
    for i in range(nKeyWords):
        keys.append(generateRandomKey(keyLength[i]))
    for m in range(2, 7):
        print('compareKm, m=' + str(m))
        k_m_english[m-2] = getKm(m)
        for i in range(nKeyWords):
            k_m_vigenere[m-2, i] = getKm(m, encrypted=True, key=keys[i])
        k_m_vigenere_mean[m-2] = np.mean(k_m_vigenere[m - 2,:])
        k_m_vigenere_std[m - 2] = np.std(k_m_vigenere[m - 2, :])
    fig, ax = plt.subplots(1, 1, figsize=(7, 4))
    ax.plot(np.arange(2, 7), k_m_english, 'o-', color='tab:blue')
    ax.plot(np.arange(2, 7), k_m_vigenere_mean, 'ko-')
    ax.plot(np.arange(2, 7), k_m_vigenere_mean + k_m_vigenere_std, 'o--', color='silver')
    ax.plot(np.arange(2, 7), k_m_vigenere_mean - k_m_vigenere_std, 'o--', color='silver')
    ax.set_xlabel(r'$m$')
    ax.set_ylabel(r'$k_m$')
    ax.set_ylim(bottom=-0.2)
    ax.legend(['Original text', 'Mean of encrypted texts', 'Mean of encrypted texts with 1 std'], frameon=False)
    plt.savefig('km.pdf')
    plt.savefig('km.png')
    plt.show()

def compareKmWithSkip(maxKeyLength=45):
    nKeyWords = 100

    k_m_vigenere_s = np.zeros((5,nKeyWords))
    k_m_vigenere_s_mean = np.zeros(5)
    k_m_vigenere_s_std = np.zeros(5)
    k_m_vigenere_k = np.zeros((5,nKeyWords))
    k_m_vigenere_k_mean = np.zeros(5)
    k_m_vigenere_k_std = np.zeros(5)

    keyLength = np.random.randint(2, maxKeyLength + 1, nKeyWords)
    s = np.random.randint(2, maxKeyLength + 1, nKeyWords)
    for w in range(nKeyWords):
        while s[w] == keyLength[w] or s[w] % keyLength[w] == 0 or keyLength[w] % s[w] == 0:
            s[w] = np.random.randint(2, maxKeyLength + 1)
    keys = []
    for i in range(nKeyWords):
        keys.append(generateRandomKey(keyLength[i]))
    for m in range(2, 7):
        print('compareKmWithSkip, m=' + str(m))
        for i in range(nKeyWords):
            k_m_vigenere_k[m - 2, i] = getKm(m, encrypted=True, key=keys[i], s=keyLength[i])
            k_m_vigenere_s[m - 2, i] = getKm(m, encrypted=True, key=keys[i], s=s[i])
        k_m_vigenere_k_mean[m - 2] = np.mean(k_m_vigenere_k[m - 2, :])
        k_m_vigenere_k_std[m - 2] = np.std(k_m_vigenere_k[m - 2, :])
        k_m_vigenere_s_mean[m - 2] = np.mean(k_m_vigenere_s[m - 2, :])
        k_m_vigenere_s_std[m - 2] = np.std(k_m_vigenere_s[m - 2, :])
    fig, ax = plt.subplots(1, 1, figsize=(5.5, 4))
    ax.plot(np.arange(2, 7), k_m_vigenere_k_mean, 's-', color='tab:blue')
    ax.plot(np.arange(2, 7), k_m_vigenere_s_mean, 'ko-')
    ax.set_xlabel(r'$m$')
    ax.set_ylabel(r'Mean $k_m$')
    ax.set_ylim(bottom=-0.6)
    ax.legend(['Letters in same state', 'Letters in differents states'], frameon=False)
    plt.savefig('km_with_skip.pdf')
    plt.savefig('km_with_skip.png')
    plt.close()

def getEntropy(text):
    letterDistribution = getLetterStatisticsInText(text)

    s = 0
    for p in letterDistribution:
        if p != 0:
            s += p*np.log2(1/p)
    return s

def compareEntropy(maxKeyLength=45):
    path = './Grimm stories/*'
    files = glob.glob(path + "/*.txt")
    s_original_list = np.zeros(len(files))
    s_vigenere_list = np.zeros(len(files))
    i = -1
    for file in files:
        i += 1
        text = getText(file)
        s_original_list[i] = getEntropy(text)
        keyLength = np.random.randint(2, maxKeyLength + 1)
        key = generateRandomKey(keyLength)
        text_vigenere = vigenereEncryption(text, key)
        s_vigenere_list[i] = getEntropy(text_vigenere)
    print(str(np.mean(s_original_list)))
    print(str(np.mean(s_vigenere_list)))
    plt.plot(s_original_list)
    plt.plot(s_vigenere_list)
    plt.legend(['Original text', 'Vigenère encrypted text'])
    plt.ylim(bottom=0)
    plt.show()

#compareEntropy()
compareKmWithSkip(20)
#compareKm(20)