import numpy as np
import matplotlib.pyplot as plt
import glob
import scipy.signal as sgn
from TextHandler import getText, getAlphabet
from encrypt import vigenereEncryption
from GetStatistics import getLetterStatisticsInText

plt.rcParams['font.size'] = 16

def get2SymbolSequenceDistributionInText(text):
    alphabet, A = getAlphabet()
    distribution = np.zeros((A, A))

    M = len(text)

    for j in range(0, M-1):
        distribution[alphabet.index(text[j]), alphabet.index(text[j+1])] += 1
    return distribution/np.sum(distribution)

def getK2fori(text, i):
    A = getAlphabet()[1]
    k2 = 0
    for j in range(i):
        subText = text[j::i]

        letterDistribution = getLetterStatisticsInText(subText)
        letterSequenceDistribution = get2SymbolSequenceDistributionInText(subText)

        for x1 in range(A):
            for x2 in range(A):
                p_x1x2 = letterSequenceDistribution[x1, x2]
                if p_x1x2 != 0:
                    p_x1 = letterDistribution[x1]
                    p_x2 = letterDistribution[x2]
                    k2 += p_x1x2*np.log2(p_x1x2/(p_x1*p_x2))/i

    return k2

def findKeyLengthCorrelations(message, maxKeyLength=45):
    k2_list = np.zeros(maxKeyLength)
    for i in range(2, maxKeyLength+2):
        k2_list[i-2] = getK2fori(message, i)
    iPeaks = sgn.find_peaks(-k2_list, threshold=0.2*np.max(k2_list))[0]
    nNonMostFrequentModMax = np.inf
    for i in range(2, maxKeyLength + 1):  # For loop for determining which modulus-operator gives most of one value => key length
        iModPeak = iPeaks % i
        counts = np.bincount(iModPeak)
        mostFrequentMod = np.argmax(counts)
        nNonMostFrequentMod = len(np.where(iModPeak != mostFrequentMod)[0])
        if nNonMostFrequentMod <= nNonMostFrequentModMax:
            nNonMostFrequentModMax = nNonMostFrequentMod
            keylength = i

    print('Key length is ' + str(keylength))
    plt.plot(np.linspace(2,maxKeyLength+1, maxKeyLength), k2_list)
    plt.plot(np.arange(2, len(k2_list)+3)[iPeaks], k2_list[iPeaks], 'ro')
    plt.xlabel(r'Distance between two subsequent subtext-letters in original text')
    plt.xlabel(r'$k_2$ for subtext')
    plt.show()

def main():
    #text = getText('./Grimm stories/Testdata/IronHans.txt')
    text = getText('./Grimm stories/Testdata/TheFoxAndTheHorse.txt')
    message = vigenereEncryption(text, 'information')
    findKeyLengthCorrelations(message)
    return 0

if __name__ == '__main__':
    main()

# K2 dippar för rätt key length är för att k_corr = log \nu - s, och k_m kommer vara signifikant för många m i en vanlig
# text (korrelationer går långt in) och om s är konstant måsye k_2 vara mindre för att göra plats för de andra k_m

