import numpy as np
import matplotlib.pyplot as plt
import glob
from TextHandler import getText, getAlphabet
from encrypt import vigenereEncryption, generateRandomKey
from GetStatistics import getLetterStatisticsInText

plt.rcParams['font.size'] = 16

def getDistributions(m, encrypted, key):
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


def getKm(m, encrypted=False, key='a'):
    distribution_m, distribution_m1, distribution_m2 = getDistributions(m, encrypted, key)

    path = './Grimm stories/*'
    files = glob.glob(path + "/*.txt")
    alphabet, A = getAlphabet()

    k_m = 0
    for file in files:
        text = getText(file)
        if encrypted:
            text = vigenereEncryption(text, key)
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
    k_m_english = np.zeros(5)
    k_m_vigenere = np.zeros((5,10))
    k_m_vigenere_mean = np.zeros(5)
    k_m_vigenere_std = np.zeros(5)

    keyLength = np.random.randint(2, maxKeyLength + 1, 10)
    keys = []
    for i in range(10):
        keys.append(generateRandomKey(keyLength[i]))
    print(keys)
    for m in range(2, 7):
        k_m_english[m-2] = getKm(m)
        print('In standard english k_' + str(int(m)) + '=' + str(np.round_(k_m_english[m - 2], 4)))
        for i in range(10):
            k_m_vigenere[m-2, i] = getKm(m, encrypted=True, key=keys[i])
        k_m_vigenere_mean[m-2] = np.mean(k_m_vigenere[m - 2,:])
        k_m_vigenere_std[m - 2] = np.std(k_m_vigenere[m - 2, :])
        print('In vigenere english k_' + str(int(m)) + '=' + str(np.round_(k_m_vigenere_mean[m-2], 4)))
    plt.plot(np.arange(2, 7), k_m_english, 'o-', color='tab:blue')
    plt.plot(np.arange(2, 7), k_m_vigenere_mean, 'ko-')
    plt.plot(np.arange(2, 7), k_m_vigenere_mean + k_m_vigenere_std, 'o--', color='silver')
    plt.plot(np.arange(2, 7), k_m_vigenere_mean - k_m_vigenere_std, 'o--', color='silver')
    plt.xlabel(r'$m$')
    plt.ylabel(r'$k_m$')
    #plt.title('Key is ' + key)
    plt.legend(['Original text', 'Mean of encrypted texts', 'Mean of encrypted texts with 1 std'])
    plt.show()


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
    plt.plot(s_original_list)
    plt.plot(1.2*s_original_list)
    plt.plot(s_vigenere_list)
    plt.legend(['s_original', '1.2s_original', 's_vigenere'])
    plt.show()

#compareEntropy()
compareKm(10)