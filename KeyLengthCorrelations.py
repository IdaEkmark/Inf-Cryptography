import numpy as np
import matplotlib.pyplot as plt
import glob
import scipy.signal as sgn
from TextHandler import getText, getAlphabet
from encrypt import vigenereEncryption, generateRandomKey
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

def findKeyLengthCorrelations(message, maxKeyLength=45, plot=False):
    k2_list = np.zeros(maxKeyLength)
    for i in range(2, maxKeyLength+2):
        k2_list[i-2] = getK2fori(message, i)
    k2_list_modified = -k2_list/np.log(np.linspace(2,maxKeyLength+1, maxKeyLength))
    t = 0.3
    iPeaks = sgn.find_peaks(k2_list_modified, threshold=t * np.max(-k2_list_modified))[0]#threshold=t*np.max(-k2_list_modified))[0]
    while len(iPeaks) == 0 and t > 0.01:
        t *= 0.55
        iPeaks = sgn.find_peaks(k2_list_modified, threshold=t * np.max(-k2_list_modified))[0]
    #'''
    if plot:
        plt.plot(np.linspace(2,maxKeyLength+1, maxKeyLength), k2_list_modified)
        plt.plot(np.arange(2, len(k2_list)+3)[iPeaks], k2_list_modified[iPeaks], 'ro')
        plt.xlabel(r'Distance between two subsequent subtext-letters in original text')
        plt.xlabel(r'$k_2$ for subtext')
        plt.show()
    if len(iPeaks) == 0:
        return -1
    nNonMostFrequentModMax = np.inf
    if len(iPeaks) == 1:
        keylength = iPeaks[0] + 2
    else:
        for i in range(2, maxKeyLength + 1):  # For loop for determining which modulus-operator gives most of one value => key length
            iModPeak = iPeaks % i
            counts = np.bincount(iModPeak)
            mostFrequentMod = np.argmax(counts)
            nNonMostFrequentMod = len(np.where(iModPeak != mostFrequentMod)[0])
            if nNonMostFrequentMod <= nNonMostFrequentModMax:
                nNonMostFrequentModMax = nNonMostFrequentMod
                keylength = i
    if plot:
        print('Key length is ' + str(keylength))
        plt.plot(np.linspace(2,maxKeyLength+1, maxKeyLength), k2_list)
        plt.plot(np.arange(2, len(k2_list)+3)[iPeaks], k2_list[iPeaks], 'ro')
        plt.xlabel(r'Distance between two subsequent subtext-letters in original text')
        plt.xlabel(r'$k_2$ for subtext')
        plt.show()
    return keylength

def main():
    i = 0
    e = 0
    path = './Grimm stories/Trainingdata_Statistics'
    files = glob.glob(path + "/*.txt")
    nFiles = len(files)
    iFile = np.random.randint(nFiles)
    text = getText(files[iFile])
    while True:
        i += 1
        #print(str(i))
        #'''
        if i % 2 == 0:
            kl = np.random.randint(2, 3)#46)
        elif i % 2 == 1:
            kl = np.random.randint(14, 17)
        else:
            kl = np.random.randint(30, 46)  # 46)
        #'''
        #kl = np.random.randint(2, 46)
        key = generateRandomKey(kl)
        message = vigenereEncryption(text, key)
        klC = findKeyLengthCorrelations(message, plot=True)
        print('kl = ' + str(kl) + ', found kl = ' + str(klC))
        if klC != kl:
            e+= 1
            print(str(e/i))
    return 0

if __name__ == '__main__':
    main()

# K2 dippar för rätt key length är för att k_corr = log \nu - s, och k_m kommer vara signifikant för många m i en vanlig
# text (korrelationer går långt in) och om s är konstant måsye k_2 vara mindre för att göra plats för de andra k_m

